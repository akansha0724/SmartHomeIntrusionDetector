# GitHub Push Instructions

Your project is ready to push! Follow these steps:

## Option 1: Using GitHub Web Interface (Easiest)

1. **Create new repository on GitHub:**
   - Go to [github.com/new](https://github.com/new)
   - Repository name: `SmartHomeIntrusionDetector`
   - Description: `AI-based smart home network intrusion detection with SHAP explainability and email alerts`
   - Make it **Public** (so others can see/use it)
   - Click **Create repository**

2. **Copy the HTTPS URL from GitHub** (looks like `https://github.com/YOUR_USERNAME/SmartHomeIntrusionDetector.git`)

3. **In PowerShell, run:**
   ```powershell
   cd 'c:\Users\akans\OneDrive\Desktop\SmartHomeIntrusionDetector'
   git remote remove origin
   git remote add origin https://github.com/YOUR_USERNAME/SmartHomeIntrusionDetector.git
   git branch -M main
   git push -u origin main
   ```

4. **GitHub will prompt for authentication:**
   - Click "Authorize" if a browser window opens, OR
   - Enter your GitHub username when prompted
   - For password, use a **Personal Access Token** (see below)

## Getting a GitHub Personal Access Token

If authentication fails:

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name it: `GitHub Push Token`
4. Check these scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (update GitHub Action workflows)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. When Git prompts for password, paste this token

## Option 2: Using GitHub CLI (Alternative)

If you have GitHub CLI installed:

```powershell
gh auth login
# Follow prompts to authenticate

cd 'c:\Users\akans\OneDrive\Desktop\SmartHomeIntrusionDetector'
git remote remove origin
gh repo create SmartHomeIntrusionDetector --public --source=. --remote=origin --push
```

## Verify Success

After pushing, visit:
```
https://github.com/YOUR_USERNAME/SmartHomeIntrusionDetector
```

You should see:
- ✅ All 15+ files
- ✅ Green checkmark on CI badge (GitHub Actions running tests)
- ✅ README.md displayed
- ✅ Deployment guide available

## Next: Deploy to Streamlit Cloud

Once on GitHub:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your **SmartHomeIntrusionDetector** repo
5. Set main file: `main.py`
6. Click **Deploy**
7. Go to **Secrets** tab and add:
   ```toml
   SMTP_HOST = "smtp.gmail.com"
   SMTP_PORT = "587"
   SMTP_USER = "akansha0724@gmail.com"
   SMTP_PASSWORD = "your_app_password"
   ALERT_TO = "akansha0724@gmail.com"
   ```
8. Your app is LIVE! 🚀

**Your live app URL will be:**
```
https://akansha0724-smarthomeintrusiondetector.streamlit.app
```

---

**Need help?** Feel free to ask after you've created the GitHub repo!
