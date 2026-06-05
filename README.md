# Smart Home Intrusion Detection System

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/SHAP-FF6B6B?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Anomaly%20Detection-Isolation%20Forest-2ecc71?style=flat-square"/>
</p>

An AI-powered network security system that monitors IoT device behaviour in real time and flags suspicious activity — without requiring labelled attack data.

---

## Business Problem

Smart homes generate continuous network traffic across dozens of devices. Traditional signature-based security systems fail against novel or zero-day attacks. This system uses **unsupervised anomaly detection** to establish normal behaviour baselines per device and alert when traffic deviates — the same principle applied in financial fraud detection and healthcare network monitoring.

---

## How It Works

```
Network Traffic → Isolation Forest Model → Risk Classification → Dashboard + Alert
                        ↓
                  SHAP Explanations
                (why was this flagged?)
```

1. **Data ingestion** — traffic features (packet counts, device ID, z-score deviation) collected per device
2. **Anomaly scoring** — Isolation Forest assigns a numeric risk score (0–100) to each observation
3. **Risk classification** — scored as LOW / MEDIUM / HIGH
4. **Explainability** — SHAP KernelExplainer identifies which features drove each anomaly flag
5. **Alerting** — real-time Streamlit dashboard + optional email notifications for MEDIUM/HIGH events

---

## Key Features

| Feature | Detail |
|---|---|
| Unsupervised detection | Works without labelled attack data; catches zero-day threats |
| SHAP explainability | Every alert includes human-readable reasoning and feature contributions |
| Risk scoring | Numeric 0–100 score + categorical label for prioritisation |
| Live dashboard | Streamlit interface with traffic visualisation and alert history |
| Email alerts | SMTP integration for MEDIUM/HIGH risk notifications |
| CI/CD | GitHub Actions pipeline runs test suite on every push |

---

## Tech Stack

- **ML**: Isolation Forest (scikit-learn), SHAP KernelExplainer
- **Dashboard**: Streamlit
- **Data**: Pandas, NumPy
- **Testing**: pytest + GitHub Actions
- **Alerts**: SMTP email integration

---

## Project Structure

```
├── main.py                  # Streamlit dashboard
├── anomaly_detector.py      # Isolation Forest model + SHAP logic
├── alerts.py                # Email alert system
├── simulate_traffic.py      # Network traffic simulator for demo/testing
├── tests/                   # pytest test suite
├── .github/workflows/       # CI/CD pipeline
├── DEPLOYMENT.md            # Deployment guide (Streamlit Cloud, Docker, Azure)
└── requirements.txt
```

---

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run main.py
```

The app opens at `http://localhost:8501`.

---

## Email Alerts (Optional)

Set environment variables before running:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_TO=recipient@example.com
```

For local testing without real SMTP: `python debug_smtp_server.py` prints emails to console.

---

## Relevance to Analytics Roles

The anomaly detection methodology here is directly applicable to:
- **Financial services** — transaction fraud detection, unusual account behaviour
- **Healthcare** — medical device network monitoring, EMR access anomalies
- **Operations analytics** — infrastructure monitoring, SLA breach prediction
