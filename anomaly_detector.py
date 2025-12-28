from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np


def detect_anomalies(df, historical_df=None):
    """Detect anomalies and produce explainable outputs.

    Returns a DataFrame with additional columns:
      - DeviceID, Anomaly, AnomalyScore (0-1), RiskScore (0-100), Risk (LOW/MEDIUM/HIGH),
        Explanation (text), CyberContext (mapped scenario), Quarantine
    """
    df = df.copy()
    # Ensure timestamp dtype
    if not np.issubdtype(df['Timestamp'].dtype, np.datetime64):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Device codes
    df['DeviceID'] = df['Device'].astype('category').cat.codes

    # Build baseline stats per device from historical data if available, else from df
    if historical_df is not None and not historical_df.empty:
        hist = historical_df.copy()
        if not np.issubdtype(hist['Timestamp'].dtype, np.datetime64):
            hist['Timestamp'] = pd.to_datetime(hist['Timestamp'])
        combined = pd.concat([hist[['Device', 'Packets']], df[['Device', 'Packets']]], ignore_index=True)
    else:
        combined = df[['Device', 'Packets']]

    baseline = combined.groupby('Device')['Packets'].agg(['mean', 'std']).reset_index().rename(columns={'mean': 'BaselineMean', 'std': 'BaselineStd'})
    df = df.merge(baseline, on='Device', how='left')
    df['BaselineStd'] = df['BaselineStd'].fillna(0.0)

    # Z-score relative to device baseline
    df['Z'] = (df['Packets'] - df['BaselineMean']) / (df['BaselineStd'] + 1e-6)

    # Features for isolation forest
    X = df[['DeviceID', 'Packets', 'Z']]

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    df['Anomaly'] = model.predict(X)  # -1 for anomaly, 1 for normal

    # Decision function -> anomaly magnitude (lower -> more anomalous)
    dec = model.decision_function(X)
    # convert to anomaly score where higher means more anomalous
    anomaly_raw = -dec
    # normalize 0-1
    minv, maxv = anomaly_raw.min(), anomaly_raw.max()
    if maxv - minv <= 0:
        df['AnomalyScore'] = 0.0
    else:
        df['AnomalyScore'] = (anomaly_raw - minv) / (maxv - minv)

    # Numeric risk score: combine anomaly score and z-score magnitude
    z_norm = np.tanh(np.abs(df['Z']) / 3.0)  # squash z into 0-1
    df['RiskScore'] = (0.7 * df['AnomalyScore'] + 0.3 * z_norm) * 100
    df['RiskScore'] = df['RiskScore'].round(1)

    # Categorical risk
    def categorize(score):
        if score >= 70:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'

    df['Risk'] = df['RiskScore'].apply(categorize)

    # Explanation generation
    explanations = []
    cyber_contexts = []
    packets_99 = df['Packets'].quantile(0.99)
    for _, row in df.iterrows():
        reasons = []
        context = 'Unknown'

        if row['Packets'] > (row['BaselineMean'] + 3 * (row['BaselineStd'] + 1e-6)):
            reasons.append('Unusually high packet transmission')

        if abs(row['Z']) > 2:
            reasons.append('Sudden deviation from device baseline')

        if row['Packets'] > packets_99:
            reasons.append('Abnormal traffic compared to other devices')
            # possible DDoS if many devices simultaneously have high packets — flagged later by aggregator

        hour = row['Timestamp'].hour
        if hour < 6 and row['Anomaly'] == -1:
            reasons.append('Anomalous activity during odd hours')

        # Map to simple cybersecurity contexts
        if row['Packets'] > row['BaselineMean'] * 5:
            context = 'Possible Botnet Activity'
        elif row['Packets'] > packets_99:
            context = 'Possible DDoS or Flood'
        elif row['Risk'] == 'HIGH':
            context = 'Potential Unauthorized Access'

        explanations.append('; '.join(reasons) if reasons else 'Anomaly detected by model')
        cyber_contexts.append(context)

    df['Explanation'] = explanations
    df['CyberContext'] = cyber_contexts

    # Quarantine decision
    df['Quarantine'] = df['Risk'].apply(lambda x: 'Yes' if x == 'HIGH' else 'No')

    # Optional: SHAP-based explanations for top anomalies (best-effort)
    df['SHAP_Explanation'] = ''
    try:
        import shap

        # Use a small background sample
        bg = X.sample(n=min(50, len(X)), random_state=42).to_numpy()
        # model function expects array-like -> returns decision_function
        def model_fn(data_array):
            try:
                d = pd.DataFrame(data_array, columns=X.columns)
                return model.decision_function(d)
            except Exception:
                # fallback shape
                return np.zeros((data_array.shape[0],))

        explainer = shap.KernelExplainer(model_fn, bg)

        # Compute SHAP values only for top anomalous rows to save time
        anomalous_idx = df[df['Anomaly'] == -1].sort_values('AnomalyScore', ascending=False).head(10).index
        if len(anomalous_idx) > 0:
            X_subset = X.loc[anomalous_idx].to_numpy()
            # nsamples can be tuned; keep small for speed
            shap_vals = explainer.shap_values(X_subset, nsamples=100)
            feature_names = list(X.columns)
            for i, idx in enumerate(anomalous_idx):
                vals = shap_vals[i]
                # pair feature and contribution
                pairs = list(zip(feature_names, vals))
                # sort by absolute contribution
                pairs.sort(key=lambda x: abs(x[1]), reverse=True)
                # take top 2 contributors
                top = pairs[:2]
                expl_text = ', '.join([f"{name}:{val:.3f}" for name, val in top])
                df.at[idx, 'SHAP_Explanation'] = expl_text
    except Exception:
        # If SHAP is not available or fails, skip without breaking
        pass

    return df
