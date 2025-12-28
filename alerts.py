import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
import ssl
from email.message import EmailMessage

# Public exports
__all__ = ["send_alert", "show_alert_dashboard"]

def send_alert(device, packets, risk, risk_score=None, explanation=None, shap_explanation=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    st.session_state.alerts.append({
        "Time": timestamp,
        "Device": device,
        "Packets": int(packets),
        "Risk": risk,
        "RiskScore": risk_score,
        "Explanation": explanation,
        "SHAP_Explanation": shap_explanation
    })

    if risk == "HIGH":
        st.error(f"🚨 HIGH RISK intrusion on {device}")
        _maybe_send_email(device, packets, risk, timestamp, risk_score, explanation, shap_explanation)
    elif risk == "MEDIUM":
        st.warning(f"⚠️ Suspicious activity on {device}")
        _maybe_send_email(device, packets, risk, timestamp, risk_score, explanation, shap_explanation)
    else:
        st.info(f"ℹ️ Unusual activity on {device}")


def show_alert_dashboard():
    st.subheader("🔔 Intrusion Alert Dashboard")

    if "alerts" not in st.session_state:
        st.success("✅ No alerts detected")
        return

    df = pd.DataFrame(st.session_state.alerts)
    # Normalize Time to datetime if possible
    try:
        df['Time'] = pd.to_datetime(df['Time'])
    except Exception:
        pass

    st.dataframe(df, use_container_width=True)

    # Trend: alerts over time
    if 'Time' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Time']):
        counts = df.set_index('Time').resample('1T').size()
        if not counts.empty:
            st.line_chart(counts.rename('Alerts per minute'))

    # Detailed view with SHAP explanations for each HIGH/MEDIUM alert
    st.subheader("📊 Alert Details & Feature Importance")
    for idx, row in df.iterrows():
        if row.get('Risk') in ['HIGH', 'MEDIUM']:
            with st.expander(f"Device: {row.get('Device')} | Risk: {row.get('Risk')} | Score: {row.get('RiskScore', 'N/A')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Time:** {row.get('Time')}")
                    st.write(f"**Packets:** {row.get('Packets')}")
                    st.write(f"**Risk Score:** {row.get('RiskScore', 'N/A')}/100")
                with col2:
                    st.write(f"**Explanation:** {row.get('Explanation', 'N/A')}")
                    st.write(f"**Cyber Context:** {row.get('CyberContext', 'Unknown')}")
                if row.get('SHAP_Explanation'):
                    st.write(f"**Feature Importance (SHAP):** {row.get('SHAP_Explanation')}")


def _maybe_send_email(device, packets, risk, timestamp, risk_score=None, explanation=None, shap_explanation=None):
    """Send an email alert if SMTP configuration is present in environment.

    Required environment variables:
      - SMTP_HOST
      - SMTP_PORT
      - SMTP_USER
      - SMTP_PASSWORD
      - ALERT_TO  (comma-separated recipient emails)

    If `SMTP_HOST` is not set, this function returns silently.
    """
    # Prefer settings provided in Streamlit session state (set via UI), fall back to env vars
    smtp_cfg = None
    try:
        smtp_cfg = st.session_state.get("smtp_config")
    except Exception:
        smtp_cfg = None

    if smtp_cfg:
        smtp_host = smtp_cfg.get("SMTP_HOST")
        smtp_port = int(smtp_cfg.get("SMTP_PORT", 587))
        smtp_user = smtp_cfg.get("SMTP_USER")
        smtp_password = smtp_cfg.get("SMTP_PASSWORD")
        alert_to = smtp_cfg.get("ALERT_TO")
    else:
        # Check Streamlit secrets next (secure for deployment)
        # Safely attempt to read Streamlit secrets (may raise if no secrets file)
        try:
            secrets = getattr(st, "secrets", None)
        except Exception:
            secrets = None

        has_secrets = False
        smtp_host_secret = None
        alert_to_secret = None
        if secrets is not None:
            try:
                smtp_host_secret = secrets.get("SMTP_HOST")
                alert_to_secret = secrets.get("ALERT_TO")
                has_secrets = bool(smtp_host_secret or alert_to_secret)
            except Exception:
                has_secrets = False

        if has_secrets:
            smtp_host = smtp_host_secret
            smtp_port = int(secrets.get("SMTP_PORT", 587))
            smtp_user = secrets.get("SMTP_USER")
            smtp_password = secrets.get("SMTP_PASSWORD")
            alert_to = alert_to_secret
        else:
            smtp_host = os.getenv("SMTP_HOST")
            if not smtp_host:
                return
            try:
                smtp_port = int(os.getenv("SMTP_PORT", "587"))
            except ValueError:
                smtp_port = 587
            smtp_user = os.getenv("SMTP_USER")
            smtp_password = os.getenv("SMTP_PASSWORD")
            alert_to = os.getenv("ALERT_TO")

    if not alert_to:
        st.warning("Email alert configured but `ALERT_TO` not set; skipping email.")
        return

    recipients = [addr.strip() for addr in alert_to.split(",") if addr.strip()]
    if not recipients:
        st.warning("No valid recipient addresses found in `ALERT_TO`.")
        return

    subject = f"[{risk}] Intrusion alert — {device}"
    body_lines = [
        f"Time: {timestamp}",
        f"Device: {device}",
        f"Packets: {packets}",
        f"Risk: {risk}",
    ]
    if risk_score is not None:
        body_lines.append(f"RiskScore: {risk_score}")
    if explanation:
        body_lines.append(f"Explanation: {explanation}")
    if shap_explanation:
        body_lines.append(f"Feature Importance (SHAP): {shap_explanation}")

    body_lines.append("")
    body_lines.append("This is an automated alert from Smart Home Intrusion Detector.")
    body = "\n".join(body_lines)

    msg = EmailMessage()
    msg["From"] = smtp_user or f"alerts@{smtp_host}"
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls(context=context)
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(msg)
        st.info(f"Email alert sent to: {', '.join(recipients)}")
    except OSError as e:
        # DNS/Network error: getaddrinfo failed, connection refused, etc.
        st.error(f"❌ Network error sending alert to {smtp_host}:{smtp_port}: {e}")
        st.info(
            "**Troubleshooting DNS Error:**\n"
            "1. Check hostname spelling (e.g., 'smtp.gmail.com' not 'gmail.com')\n"
            "2. Test with Gmail: Use 'smtp.gmail.com:587' + App Password\n"
            "3. Try local debug SMTP server:\n"
            "   - Run: `python -m smtpd -n -c DebuggingServer localhost:1025`\n"
            "   - Set SMTP Host: 'localhost', Port: '1025'\n"
            "   - Emails will print to console, not send\n"
            "4. Check firewall/network blocks port 587 (SMTP)\n"
            "5. Verify internet connection"
        )
        return False, str(e)
    except smtplib.SMTPAuthenticationError as e:
        st.error(f"❌ Authentication failed for {smtp_user}: {e}")
        st.info(
            "**Fix authentication:**\n"
            "- Gmail: Use App Password, not account password\n"
            "- Verify User and Password are correct\n"
            "- Check SMTP Port matches auth method (587 for TLS)"
        )
        return False, str(e)
    except Exception as e:
        st.error(f"Failed to send email alert: {e}")
        return False, str(e)
    return True, 'OK'


def test_smtp_connection():
    """Attempt to connect to configured SMTP server and return (ok, message).

    Uses session_state smtp_config, then st.secrets, then env vars (same as _maybe_send_email).
    This helper is safe to call from the Streamlit app UI.
    """
    # Reuse the same resolution logic as _maybe_send_email
    try:
        cfg = st.session_state.get('smtp_config')
    except Exception:
        cfg = None

    if cfg:
        smtp_host = cfg.get('SMTP_HOST')
        smtp_port = int(cfg.get('SMTP_PORT') or 587)
        smtp_user = cfg.get('SMTP_USER')
        smtp_password = cfg.get('SMTP_PASSWORD')
    else:
        try:
            secrets = getattr(st, 'secrets', None)
        except Exception:
            secrets = None

        smtp_host = None
        smtp_port = 587
        smtp_user = None
        smtp_password = None
        if secrets is not None:
            try:
                smtp_host = secrets.get('SMTP_HOST')
                smtp_port = int(secrets.get('SMTP_PORT', 587))
                smtp_user = secrets.get('SMTP_USER')
                smtp_password = secrets.get('SMTP_PASSWORD')
            except Exception:
                pass

        if not smtp_host:
            smtp_host = os.getenv('SMTP_HOST')
            try:
                smtp_port = int(os.getenv('SMTP_PORT', smtp_port))
            except Exception:
                smtp_port = smtp_port
            smtp_user = os.getenv('SMTP_USER')
            smtp_password = os.getenv('SMTP_PASSWORD')

    if not smtp_host:
        return False, 'No SMTP host configured (set via sidebar, secrets, or env vars)'

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls(context=context)
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
        return True, f'Connected to {smtp_host}:{smtp_port}'
    except Exception as e:
        return False, f'Failed to connect to {smtp_host}:{smtp_port} — {e}'
