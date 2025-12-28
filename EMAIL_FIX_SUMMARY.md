# Email Alert DNS Error - FIXED ✅

## Problem
You were getting a DNS resolution error when trying to send email alerts:
```
Failed to send email alert to akansha0724@gmail.com: [Errno 11003] getaddrinfo failed
```

## Root Cause
The error `[Errno 11003] getaddrinfo failed` is a network/DNS issue that occurs when:
- The SMTP hostname cannot be resolved by DNS
- Network/firewall blocks outbound SMTP connections
- The hostname is invalid or misspelled

## Solutions Implemented

### 1. **Improved Error Handling** (`alerts.py`)
- Added specific exception handling for `OSError` (network/DNS errors)
- Separated authentication errors from network errors for clearer diagnosis
- Each error type now shows actionable troubleshooting steps in the UI

### 2. **Local Debug SMTP Server** (`debug_smtp_server.py`)
Created a new helper script that runs a local SMTP server for testing:
```powershell
# Terminal 1: Start the debug server
python debug_smtp_server.py

# Terminal 2: Run Streamlit with local SMTP (PowerShell)
$env:SMTP_HOST='localhost'
$env:SMTP_PORT='1025'
$env:ALERT_TO='test@example.com'
streamlit run main.py
```

All emails will print to the console instead of being sent over the network.

### 3. **Comprehensive Troubleshooting Guide** (`README.md`)
Added detailed troubleshooting section with:
- DNS resolution error fixes
- Authentication failure solutions
- Network connectivity tests
- Gmail configuration steps
- Firewall bypass options
- SHAP missing explanations troubleshooting

## How to Fix Your Issue

### Option 1: Use Gmail (Recommended)
1. Go to [Google Account Security](https://myaccount.google.com/apppasswords)
2. Generate an App Password (not your regular password)
3. In Streamlit Email Settings sidebar, configure:
   - SMTP Host: `smtp.gmail.com`
   - SMTP Port: `587`
   - SMTP User: Your Gmail address
   - SMTP Password: The app password you just generated
   - Alert To: `akansha0724@gmail.com`
4. Click "Test SMTP connection" to verify

### Option 2: Use Local Debug Server (No Internet Required)
1. Open Terminal 1 and run:
   ```powershell
   python debug_smtp_server.py
   ```
2. Open Terminal 2 (in the project folder) and run:
   ```powershell
   $env:SMTP_HOST='localhost'
   $env:SMTP_PORT='1025'
   $env:ALERT_TO='akansha0724@gmail.com'
   streamlit run main.py
   ```
3. Trigger an alert in the app - the email will print in Terminal 1

### Option 3: Verify Network Connectivity
Test your network can reach the SMTP server:
```powershell
nslookup smtp.gmail.com
Test-NetConnection -ComputerName smtp.gmail.com -Port 587
```

## Testing
All tests pass ✅:
```powershell
pytest tests/test_alerts_email.py -v
# Result: 1 passed
```

The SMTP error handling now gracefully catches DNS errors and provides users with clear troubleshooting steps.

## Files Modified
1. **alerts.py** - Enhanced error handling with OS-level exception catching
2. **debug_smtp_server.py** - NEW: Local SMTP debug server script
3. **README.md** - Added comprehensive troubleshooting section

## Next Steps
1. Try one of the three solutions above
2. Click "Test SMTP connection" in the sidebar to verify setup
3. Trigger a HIGH/MEDIUM risk alert to test email sending
4. If still having issues, check the detailed error messages shown in the UI
