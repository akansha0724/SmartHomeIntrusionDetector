# GitHub Setup - Step by Step

## Step 1: Create the Repository on GitHub.com

1. Go to [github.com/new](https://github.com/new)
   (Or click the **+** icon at top right → New repository)

2. Fill in the form:
   - **Repository name:** `SmartHomeIntrusionDetector`
   - **Description:** `AI-based smart home intrusion detection with SHAP explainability and email alerts`
   - **Visibility:** Select **Public** ✅
   - **Initialize this repository with:** Leave all unchecked
   
3. Click **Create repository** button

4. You'll see a page with setup instructions. **Don't close it!**

## Step 2: Copy Your GitHub URL

After creating, you'll see something like:

```
…or push an existing repository from the command line

git remote add origin https://github.com/akansha0724/SmartHomeIntrusionDetector.git
git branch -M main
git push -u origin main
```

Your URL is: `https://github.com/akansha0724/SmartHomeIntrusionDetector.git`

## Step 3: Push Your Code

Now run in PowerShell:

```powershell
cd 'c:\Users\akans\OneDrive\Desktop\SmartHomeIntrusionDetector'
git remote remove origin
git remote add origin https://github.com/akansha0724/SmartHomeIntrusionDetector.git
git branch -M main
git push -u origin main
```

## Step 4: Authenticate

Git will prompt you for credentials. You have 2 options:

### Option A: Personal Access Token (Recommended)

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name: `SmartHome Push Token`
4. Expiration: 90 days
5. Check these boxes:
   - ✅ `repo`
   - ✅ `workflow`
6. Click **Generate token**
7. **COPY THE TOKEN** (you won't see it again!)
8. When Git asks for password, paste this token

### Option B: Web Browser Auth

- Git may open a browser window to authenticate
- Click **Authorize** and it will complete automatically

## Step 5: Verify Success

After pushing, go to:
```
https://github.com/akansha0724/SmartHomeIntrusionDetector
```

You should see:
- ✅ Your code files
- ✅ README.md displayed
- ✅ Green checkmark (CI tests passing)
- ✅ 15+ files committed

## Troubleshooting

**"Repository not found" error:**
- Make sure you created the repo on GitHub.com first
- Check that visibility is **Public**

**"Authentication failed" error:**
- Use Personal Access Token, not your password
- Get token from [github.com/settings/tokens](https://github.com/settings/tokens)

**"fatal: branch master -M main not found":**
- This usually means the remote wasn't set correctly
- Try: `git remote remove origin` then add it again

---

Once your code is on GitHub, deployment to Streamlit Cloud is just 3 clicks!
