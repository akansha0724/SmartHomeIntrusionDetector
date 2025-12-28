# Deployment Guide - Smart Home Intrusion Detector

This guide covers deploying your Smart Home Intrusion Detection System to production with email alerts working end-to-end.

## Option 1: Streamlit Cloud (Easiest)

### Prerequisites
- GitHub account with the repo uploaded
- Gmail account with App Password generated

### Step 1: Create Streamlit Cloud Account
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"

### Step 2: Deploy Your App
1. Select your repository: `SmartHomeIntrusionDetector`
2. Select branch: `main`
3. Set main file path: `main.py`
4. Click "Deploy"

The app will be live at `https://[your-username]-smarthomeintrusiondetector.streamlit.app`

### Step 3: Configure Email Alerts (Critical!)

1. In Streamlit Cloud dashboard, go to your app
2. Click the menu (⋮) → **Secrets**
3. Paste this configuration:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "akansha0724@gmail.com"
SMTP_PASSWORD = "your_gmail_app_password"
ALERT_TO = "akansha0724@gmail.com"
```

4. Click "Save"
5. Streamlit will automatically redeploy your app with these secrets

### Getting Your Gmail App Password
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in to your Google Account
3. Select **Mail** and **Windows Computer**
4. Google generates a 16-character password
5. Copy it to the `SMTP_PASSWORD` field above

### Test Email Alerts
1. Open your deployed app
2. Click "Initialize System" button
3. Click "Simulate Attack" button
4. Check your email for the HIGH risk alert
5. If email doesn't arrive, click "Test SMTP connection" in the sidebar to debug

---

## Option 2: Docker (Self-Hosted)

### Prerequisites
- Docker installed
- Server/VPS with internet access
- Gmail App Password

### Step 1: Create Dockerfile
Create a `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create .streamlit/config.toml
```toml
[server]
port = 8501
headless = true
runOnSave = true

[logger]
level = "info"
```

### Step 3: Build and Run
```bash
# Build image
docker build -t smart-home-detector .

# Run container with email credentials
docker run -d \
  -p 8501:8501 \
  -e SMTP_HOST="smtp.gmail.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USER="akansha0724@gmail.com" \
  -e SMTP_PASSWORD="your_app_password" \
  -e ALERT_TO="akansha0724@gmail.com" \
  --name detector \
  smart-home-detector
```

### Step 4: Test
- Open `http://your-server-ip:8501`
- Configure and test alerts as above

---

## Option 3: Heroku (Deprecated but Possible)

Heroku is free tier is no longer available, but you can still deploy:

### Step 1: Create Procfile
```
web: streamlit run main.py --server.port=$PORT
```

### Step 2: Deploy
```bash
heroku login
heroku create your-app-name
heroku config:set SMTP_HOST="smtp.gmail.com"
heroku config:set SMTP_PORT="587"
heroku config:set SMTP_USER="akansha0724@gmail.com"
heroku config:set SMTP_PASSWORD="your_app_password"
heroku config:set ALERT_TO="akansha0724@gmail.com"
git push heroku main
```

---

## Option 4: Azure App Service

### Step 1: Create App Service
```bash
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name detector-app --runtime "PYTHON|3.11"
```

### Step 2: Configure Environment Variables
```bash
az webapp config appsettings set --resource-group myResourceGroup \
  --name detector-app \
  --settings SMTP_HOST="smtp.gmail.com" SMTP_PORT="587" \
  SMTP_USER="akansha0724@gmail.com" SMTP_PASSWORD="your_app_password" \
  ALERT_TO="akansha0724@gmail.com"
```

### Step 3: Deploy
```bash
az webapp up --resource-group myResourceGroup --name detector-app
```

---

## Production Checklist

Before going live, verify:

- [ ] Email credentials are in environment variables (not in code)
- [ ] Gmail App Password is being used (not regular password)
- [ ] "Test SMTP connection" button works in the app
- [ ] You've tested the "Simulate Attack" button and received an email
- [ ] Dashboard shows alert history correctly
- [ ] SHAP explanations are computing (no errors in logs)
- [ ] No sensitive data in logs or error messages
- [ ] `.streamlit/secrets.toml` is in `.gitignore` (don't commit!)

---

## Troubleshooting Production Issues

### "Email not sending"
1. Check secrets/env vars are set correctly
2. Verify Gmail 2FA is enabled and App Password is used
3. Click "Test SMTP connection" button for detailed error
4. Check server logs for network issues

### "App shows 'getaddrinfo failed'"
- Network firewall may block port 587
- Contact your hosting provider about SMTP rules
- Use local debug server for testing: `python debug_smtp_server.py`

### "Alerts not generating"
1. Verify anomaly detection by checking the dashboard
2. Only HIGH/MEDIUM risk triggers email (LOW does not)
3. Check detection results section to see risk scores

### "SHAP explanations missing"
- SHAP computation is optional and may fail silently
- System falls back to rule-based explanations
- Check logs: `streamlit run main.py --logger.level=debug`

---

## Local Testing Before Deployment

Always test locally first:

```bash
# Terminal 1: Start debug SMTP server
python debug_smtp_server.py

# Terminal 2: Configure and run app
$env:SMTP_HOST='localhost'
$env:SMTP_PORT='1025'
$env:ALERT_TO='test@example.com'
streamlit run main.py
```

This lets you verify the entire flow without exposing real credentials.

---

## Environment Variables Reference

| Variable | Example | Required |
|----------|---------|----------|
| `SMTP_HOST` | `smtp.gmail.com` | Only if email needed |
| `SMTP_PORT` | `587` | Only if email needed |
| `SMTP_USER` | `akansha0724@gmail.com` | Only if email needed |
| `SMTP_PASSWORD` | `xyzabcd...` | Only if email needed |
| `ALERT_TO` | `recipient@example.com` | Only if email needed |

**Note:** If `SMTP_HOST` is not set, the app runs without email (alerts still appear in dashboard).

---

## Support

For issues during deployment:
1. Check the troubleshooting section in README.md
2. Review app logs for error messages
3. Test SMTP connection with the sidebar button
4. Use the local debug server to isolate issues
