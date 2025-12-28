# Smart Home Network Intrusion Detection System (AI-Based)

## 🔐 Project Overview

The Smart Home Network Intrusion Detection System is an AI-driven cybersecurity solution designed to protect smart home environments from suspicious and malicious network activity.

Smart homes consist of IoT devices such as cameras, smart locks, thermostats, lights, and speakers. These devices often have limited security and are highly vulnerable to cyberattacks. This project addresses that problem by continuously monitoring network traffic patterns and detecting anomalies in real time using machine learning.

Unlike traditional security systems that rely on predefined attack signatures, this system uses unsupervised learning, making it effective even against unknown or zero-day attacks.

## 🎯 Objectives

- Detect abnormal network behavior in smart home devices
- Identify potential intrusion attempts without prior attack data
- Provide real-time alerts and risk classification
- Offer a lightweight, explainable, and deployable solution for IoT environments

## ⚙️ How the System Works (Simple Flow)

1. Traffic Simulation / Collection
	- Network traffic data (packet counts per device) is generated to represent real smart home behavior.
2. Machine Learning-Based Detection
	- An Isolation Forest model analyzes the traffic to identify deviations from normal behavior.
3. Risk Classification
	- Each device’s activity is classified into:
	  - 🟢 LOW – Normal behavior
	  - 🟠 MEDIUM – Suspicious behavior
	  - 🔴 HIGH – Potential intrusion attempt
4. Alert Generation & Logging
	- Medium and High-risk activities trigger alerts which are displayed instantly on the dashboard and stored for review.
5. Visual Dashboard
	- A Streamlit-based interface shows live traffic data, detection results, and alert history.

## 🧠 Technologies Used

- Python – Core programming
- Machine Learning – Isolation Forest (unsupervised anomaly detection)
- Streamlit – Interactive web dashboard
- Pandas & NumPy – Data processing and analysis

## ⭐ Key Features

- AI-Based Anomaly Detection — Uses machine learning instead of rule-based detection; works without labeled attack data and can identify unknown threats.
- Real-Time Intrusion Alerts — Automatically flags suspicious devices; alerts categorized by risk level.
- Interactive Dashboard — Live traffic visualization and alert log with timestamps.
- Lightweight & IoT-Friendly — Minimal computational overhead; suitable for edge devices or local deployment.
- Explainable Security Decisions — Alerts based on observable traffic anomalies; easy for non-technical users to understand.

## 🚀 Why This Project is Unique

- No signature-based detection (unlike traditional IDS)
- Detects zero-day and unseen attacks
- Designed specifically for smart home & IoT environments
- Combines AI + cybersecurity + IoT
- Practical, real-world application aligned with modern cyber threats

## 🛡️ Relevance to e-Raksha / Cybersecurity

This project aligns strongly with digital safety and cyber protection initiatives by:

- Protecting personal smart devices
- Preventing unauthorized access and surveillance
- Promoting AI-based proactive security
- Addressing rising IoT cybercrime risks

## 🧪 Use Cases

- Home network security monitoring
- Smart city IoT infrastructure protection
- Early warning system for cyber intrusions
- Educational demonstration of AI in cybersecurity

## 📈 Future Enhancements

- Real network packet capture integration
- Mobile notification support
- Device-specific behavior profiling
- Integration with firewall or blocking mechanisms
- Visualization of attack trends over time

## 🏁 Conclusion

The Smart Home Network Intrusion Detection System demonstrates how artificial intelligence can enhance cybersecurity by providing intelligent, adaptive, and real-time protection for IoT environments. It is a practical, scalable, and future-ready solution addressing a critical modern security challenge.

## 🔁 Continuous Integration

A GitHub Actions workflow is included at `.github/workflows/ci.yml` to run the test suite on pushes and pull requests. It installs dependencies from `requirements.txt` and runs `pytest`.

## 🔼 Project Upgrades (Planned Enhancements)

The project roadmap includes the following upgrades to improve accuracy, transparency, and operational value:

1. Explainable AI for Intrusion Detection — Each alert will include a human-readable reason (e.g., unusually high packet transmission, sudden deviation from baseline, or abnormal traffic vs peers) to improve trust and interpretability.

2. Real-Time Attack Simulation — A toggleable simulation mode that injects abnormal traffic patterns for live demos, training, and validation of detection responsiveness.

3. Numeric Risk Scoring — In addition to categorical labels, the system will produce a numeric risk score to enable finer prioritization and automation.

4. Device-Aware Behavioral Analysis — Per-device baselines (camera, lock, thermostat, etc.) to reduce false positives by accounting for normal device-specific behavior.

5. Alert History & Trend Monitoring — Centralized storage and visualization of alerts over time for forensic analysis and trend detection.

6. Cybersecurity Context Mapping — Map anomalies to likely attack scenarios (DDoS, botnet, unauthorized access) to provide practical context for responders.

7. Alignment with Cyber Safety Initiatives — Design and documentation updates to demonstrate alignment with national and community cyber safety objectives.

If you'd like, I can start implementing these features one-by-one — tell me whether to begin with (A) Explainable AI + Numeric Scoring, (B) Real-Time Simulation + Device-Aware Baselines, or (C) Alert History + CI/Deployment integration.

## 🚀 Getting Started

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
```

2. Activate the virtual environment:

On Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

On Windows (cmd):

```cmd
.venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit dashboard:

```bash
streamlit run main.py
```

5. Open the URL shown by Streamlit (usually `http://localhost:8501`).

Notes:
- The repository includes a simple traffic simulator (`simulate_traffic.py`) and the detection logic in `anomaly_detector.py`.
- If you modify dependencies, update `requirements.txt` accordingly.

**To deploy to production**, see [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions for Streamlit Cloud, Docker, Azure, and other platforms.

## ✉️ Email Alerts (Optional)

You can enable email notifications for Medium/High risk alerts by setting the following environment variables before running the app:

- `SMTP_HOST` — SMTP server host (e.g., `smtp.gmail.com`)
- `SMTP_PORT` — SMTP server port (default `587`)
- `SMTP_USER` — SMTP username (email address)
- `SMTP_PASSWORD` — SMTP password or app-specific password
- `ALERT_TO` — Comma-separated recipient email addresses (e.g., `you@example.com,admin@example.com`)

Example (PowerShell):

```powershell
$env:SMTP_HOST = 'smtp.gmail.com'
$env:SMTP_PORT = '587'
$env:SMTP_USER = 'your_email@gmail.com'
$env:SMTP_PASSWORD = 'your_app_password'
$env:ALERT_TO = 'recipient@example.com'
streamlit run main.py
```

Notes:
- For Gmail, you may need to use an App Password and enable the appropriate account settings.
- If `SMTP_HOST` is not set, the app will still run but email sending will be skipped.

### Debugging SMTP failures

- If you see errors like `getaddrinfo failed`, verify the `SMTP_HOST` in the sidebar or `secrets.toml` and make sure your machine can resolve it.
- You can test connectivity from PowerShell:

```powershell
nslookup smtp.gmail.com
Test-NetConnection -ComputerName smtp.gmail.com -Port 587
```

- For safe local testing without a real SMTP server, run a debug SMTP server in a separate terminal:

**Method 1: Built-in Python debug server (recommended)**
```powershell
# Terminal 1: Run the debug SMTP server (prints emails to console)
python debug_smtp_server.py

# Terminal 2: Configure Streamlit and run the app (PowerShell):
$env:SMTP_HOST='localhost'
$env:SMTP_PORT='1025'
$env:ALERT_TO='test@example.com'
streamlit run main.py
```

**Method 2: Native Python smtpd module**
```powershell
# Terminal 1: Python's built-in debugging server
python -m smtpd -c DebuggingServer -n localhost:1025

# Terminal 2: Configure and run app (PowerShell):
$env:SMTP_HOST='localhost'
$env:SMTP_PORT='1025'
$env:ALERT_TO='test@example.com'
streamlit run main.py
```

The debug server will print all incoming emails to the console without actually sending them. Use this for testing alerts without real SMTP credentials.

The app also includes a "Test SMTP connection" button in the Email Settings sidebar to verify SMTP connectivity from the running app.

## 🔍 Explainability & Feature Importance (SHAP)

The system now uses SHAP (SHapley Additive exPlanations) to explain individual anomaly detections:

- **Rule-Based Explanations:** Each alert includes a human-readable explanation (e.g., "Unusually high packet transmission; Sudden deviation from device baseline").
- **SHAP Feature Importance:** For the top anomalies, the system computes which input features (DeviceID, Packets, Z-score) contributed most to the anomaly score.
- **Dashboard Integration:** In the Intrusion Alert Dashboard, each HIGH/MEDIUM alert has an expander that shows:
  - Numeric risk score (0–100)
  - Human explanation
  - Cyber context mapping (e.g., "Possible Botnet Activity")
  - SHAP feature contributions
  
This combination of rule-based and model-agnostic explanations ensures that both technical and non-technical users can understand *why* the system flagged an activity as anomalous.

### Technical Details

- SHAP uses a KernelExplainer on top of the Isolation Forest model.
- To keep inference fast, SHAP explanations are computed only for the top 10 anomalies per run.
- If SHAP fails or is not installed, the system gracefully falls back to rule-based explanations only.

## 🛡️ Alignment with Cyber Safety Initiatives (e-Raksha)

This Smart Home Intrusion Detection System directly supports national and community cyber safety objectives:

### 1. Protection of Personal Smart Devices
The system continuously monitors home networks, identifying unauthorized access, botnet activity, and DDoS attempts targeting personal IoT devices like cameras, locks, thermostats, and speakers.

### 2. Prevention of Unauthorized Surveillance
By detecting unusual traffic patterns, the system can alert users to potential surveillance attempts or data exfiltration from compromised devices.

### 3. Proactive Cybercrime Prevention
Instead of reactive threat response, the system uses AI to *predict* intrusions before they escalate, reducing recovery time and damage.

### 4. IoT-Centric Security
The system is specifically designed for smart home and IoT environments, which face unique vulnerabilities due to:
- Limited computational resources for complex security
- Minimal user intervention capability
- Diverse device types and behaviors
- Increasing prevalence of IoT-based botnets (Mirai, Hajime, etc.)

### 5. Transparency & Trust
All alerts include explainable AI outputs (SHAP, rule-based reasoning), ensuring that homeowners and administrators understand the system's decisions — a cornerstone of ethical AI and cyber safety.

### 6. Educational & Demonstrable Value
The system is lightweight and can be deployed for:
- Cybersecurity training and awareness
- Live demonstrations at academic and community events
- Real-world deployment in smart homes and small offices

### 7. Alignment with Digital India & e-Raksha Goals
- **Cyber Awareness:** Helps users understand network threats
- **Digital Safety:** Protects critical home infrastructure from cyber attacks
- **AI for Good:** Demonstrates responsible, interpretable AI in a safety-critical domain
- **Inclusive Security:** Accessible design for non-technical users

---

This project exemplifies how AI and cybersecurity can work together to create a safer, more resilient digital ecosystem for individuals and communities.

### Using Streamlit Secrets (recommended)

For deployment or to avoid placing SMTP credentials in environment variables, use Streamlit Secrets.
Create a `.streamlit/secrets.toml` file in the project root (do not commit it). You can start from the included example:

- [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example)

Example `secrets.toml`:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
ALERT_TO = "you@example.com"
```

The app will use `st.session_state['smtp_config']` (from the sidebar), then `st.secrets`, then environment variables — in that order.

## 🐛 Troubleshooting Common Issues

### DNS Resolution Error: `getaddrinfo failed`

**Symptoms:** Error message like `[Errno 11003] getaddrinfo failed` when trying to send email.

**Causes:**
- Invalid or misspelled SMTP hostname (e.g., `gmail.com` instead of `smtp.gmail.com`)
- Network or firewall blocking outbound SMTP connections
- ISP or local network DNS resolution issues
- Incorrect SMTP port (use 587 for TLS, 465 for SSL)

**Solutions:**

1. **Verify hostname and DNS resolution:**
   ```powershell
   # Check if DNS can resolve the SMTP server
   nslookup smtp.gmail.com
   
   # Test network connectivity to SMTP port
   Test-NetConnection -ComputerName smtp.gmail.com -Port 587
   ```

2. **Try with Gmail:**
   - SMTP Host: `smtp.gmail.com`
   - SMTP Port: `587`
   - SMTP User: Your Gmail address
   - SMTP Password: [Generate an App Password](https://myaccount.google.com/apppasswords)

3. **Use local debug SMTP server (no internet required):**
   ```powershell
   # Terminal 1: Start the debug server
   python debug_smtp_server.py
   
   # Terminal 2: Run Streamlit with local SMTP (PowerShell)
   $env:SMTP_HOST='localhost'
   $env:SMTP_PORT='1025'
   $env:ALERT_TO='test@example.com'
   streamlit run main.py
   ```
   Emails will be printed to the debug server console instead of sent.

4. **Check firewall/network policies:**
   - Port 587 (SMTP TLS) or 465 (SMTP SSL) may be blocked by your network
   - Contact your ISP or network administrator
   - Use local debug server as workaround

### Authentication Failed

**Symptoms:** Error message like `[SMTP: Authentication failed]`

**Solutions:**
- For Gmail: Use an App Password, not your account password
- Verify username and password are correct
- Ensure SMTP port matches authentication method (587 for TLS, 465 for SSL)
- Check for typos in credentials (credentials are case-sensitive)

### No Alerts Appearing

**Symptoms:** App runs but alerts don't trigger or send.

**Solutions:**
- Ensure at least one HIGH or MEDIUM risk is detected (LOW risk alerts are not emailed)
- Check if SMTP_HOST is configured (app runs but silently skips email without it)
- Use the "Test SMTP connection" button in Email Settings sidebar
- Check Streamlit session state by adding debug output in the sidebar

### Streamlit App Won't Start

**Symptoms:** `ImportError`, `ModuleNotFoundError`, or startup errors.

**Solutions:**
```powershell
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Verify imports work
python -c "import streamlit; import pandas; import numpy; import sklearn; print('OK')"

# Run app with verbose output
streamlit run main.py --logger.level=debug
```

### SHAP Explanations Missing

**Symptoms:** "SHAP not available" or blank feature importance in alerts.

**Solutions:**
- SHAP is optional; the system falls back to rule-based explanations
- To enable SHAP: `pip install shap`
- SHAP computation is skipped if fewer than 5 anomalies are detected in a batch
- For large datasets, SHAP may be slow; this is normal

---

For additional support, check the console output and session state in Streamlit's UI, or review the detailed error messages in the email settings sidebar.

