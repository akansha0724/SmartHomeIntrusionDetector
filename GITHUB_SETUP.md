# How to Push to GitHub

Your project is now ready for GitHub! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Name it: `SmartHomeIntrusionDetector`
4. **Don't** initialize with README (we already have one)
5. Click **Create repository**

## Step 2: Push Your Code

In PowerShell, run these commands in your project folder:

```powershell
cd 'c:\Users\akans\OneDrive\Desktop\SmartHomeIntrusionDetector'

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/SmartHomeIntrusionDetector.git

# Rename branch to main (if needed)
git branch -M main

# Push code to GitHub
git push -u origin main
```

## Step 3: You're Done! 🎉

Your repository is now on GitHub at:
```
https://github.com/YOUR_USERNAME/SmartHomeIntrusionDetector
```

## What's Included:

✅ Complete source code (14 files)
✅ GitHub Actions CI workflow (runs tests on push)
✅ Email alert system with SMTP configuration
✅ SHAP-based explainability
✅ Comprehensive README with troubleshooting
✅ Deployment guide for Streamlit Cloud, Docker, Azure
✅ Unit tests with mocked SMTP
✅ `.gitignore` to protect secrets

## Important Files:

- **README.md** - Project overview and usage
- **DEPLOYMENT.md** - Step-by-step deployment instructions
- **EMAIL_FIX_SUMMARY.md** - DNS error troubleshooting
- **.gitignore** - Protects `.streamlit/secrets.toml` from being committed
- **.github/workflows/ci.yml** - Automatic testing on push

## CI/CD Already Set Up:

When you push, GitHub Actions will automatically:
- ✅ Run `pytest` to test email alerts
- ✅ Check for syntax errors
- ✅ Report test results

## Deploy to Streamlit Cloud:

Once on GitHub, deployment is just 3 clicks:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app" → select your repo from GitHub
3. Add SMTP credentials in **Secrets** section
4. Done! 🚀

Your app will be live at:
```
https://[username]-smarthomeintrusiondetector.streamlit.app
```

---

**Questions?** Check:
- README.md for project details
- DEPLOYMENT.md for production setup
- EMAIL_FIX_SUMMARY.md for email troubleshooting
