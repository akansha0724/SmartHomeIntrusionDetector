# Adding Custom Devices to Smart Home Intrusion Detector

Your app currently has simulated devices (Device_1 through Device_6). Here's how to add custom devices:

## Option 1: Simple - Edit Code (Easiest)

Modify `main.py` in the `generate_data()` function:

**Current:**
```python
devices = [f"Device_{i}" for i in range(1, 7)]  # Device_1 to Device_6
```

**Change to your devices:**
```python
devices = [
    "Living_Room_Camera",
    "Front_Door_Lock", 
    "Kitchen_Thermostat",
    "Bedroom_Motion_Sensor",
    "Garage_Light"
]
```

Then restart the app and it will use your custom device names!

---

## Option 2: Better - Add UI Form (Recommended)

Add a device configuration form in the Streamlit sidebar:

Add this code to `main.py` after the Email Settings section:

```python
# Device Configuration
with st.sidebar.expander("Device Configuration", expanded=False):
    st.caption("Add custom devices to monitor")
    new_device = st.text_input("Device Name", placeholder="e.g., Living Room Camera")
    if st.button("Add Device"):
        if new_device:
            if 'custom_devices' not in st.session_state:
                st.session_state.custom_devices = []
            if new_device not in st.session_state.custom_devices:
                st.session_state.custom_devices.append(new_device)
                st.success(f"✅ Added: {new_device}")
            else:
                st.warning(f"⚠️ {new_device} already exists")
        else:
            st.error("Please enter a device name")
    
    if 'custom_devices' in st.session_state and st.session_state.custom_devices:
        st.write("**Configured Devices:**")
        for device in st.session_state.custom_devices:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- {device}")
            with col2:
                if st.button("❌", key=f"remove_{device}"):
                    st.session_state.custom_devices.remove(device)
                    st.rerun()
```

Then modify `generate_data()` to use custom devices:

```python
def generate_data(n=100):
    # Use custom devices if provided, otherwise use defaults
    if 'custom_devices' in st.session_state and st.session_state.custom_devices:
        devices = st.session_state.custom_devices
    else:
        devices = [f"Device_{i}" for i in range(1, 7)]
    
    # Rest of function stays the same...
```

---

## Option 3: Best - Upload CSV Data (Most Realistic)

Allow users to upload their own traffic data as CSV:

**Add to sidebar:**
```python
with st.sidebar.expander("Import Traffic Data", expanded=False):
    uploaded_file = st.file_uploader("Upload CSV with traffic data", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_cols = ['DeviceID', 'Packets']
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV must have columns: {required_cols}")
            else:
                # Add timestamp if missing
                if 'Timestamp' not in df.columns:
                    df['Timestamp'] = pd.date_range(
                        end=pd.Timestamp.now(), 
                        periods=len(df), 
                        freq='min'
                    )
                
                st.session_state.traffic_data = df
                st.success(f"✅ Loaded {len(df)} records from {len(df['DeviceID'].unique())} devices")
                st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error loading file: {e}")
```

**CSV Format Example:**
```
Timestamp,DeviceID,Packets
2025-12-29 10:00:00,Living_Room_Camera,150
2025-12-29 10:01:00,Front_Door_Lock,80
2025-12-29 10:02:00,Kitchen_Thermostat,200
2025-12-29 10:03:00,Living_Room_Camera,160
```

---

## Option 4: Database/API Integration (Advanced)

For real smart home data, connect to your actual devices:

```python
import requests

def fetch_real_traffic(api_url):
    """Fetch traffic data from your smart home API"""
    try:
        response = requests.get(api_url)
        data = response.json()
        
        # Parse your API response into DataFrame
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# In sidebar:
with st.sidebar.expander("Real-Time Data", expanded=False):
    api_url = st.text_input("API Endpoint", placeholder="http://your-api.com/traffic")
    if st.button("Fetch Live Data"):
        df = fetch_real_traffic(api_url)
        if df is not None:
            st.session_state.traffic_data = df
```

---

## Recommended Approach

**For most users: Option 2 (UI Form)**
- No coding required after implementation
- Intuitive for non-technical users
- Devices saved in session state
- Easy to add/remove devices

**For data analysis: Option 3 (CSV Upload)**
- Use real historical data
- Test with actual network traffic
- No API integration needed
- Format: CSV with DeviceID and Packets columns

---

## Step-by-Step: Add Custom Devices (Option 2)

1. **Open `main.py`**

2. **Find this section:**
```python
# Email Settings UI
with st.sidebar.expander("Email Settings (optional)", expanded=False):
```

3. **Add BEFORE it:**
```python
# Device Configuration
with st.sidebar.expander("Device Configuration", expanded=False):
    st.caption("Add custom devices to monitor")
    new_device = st.text_input("Device Name", placeholder="e.g., Living Room Camera")
    if st.button("Add Device"):
        if new_device:
            if 'custom_devices' not in st.session_state:
                st.session_state.custom_devices = []
            if new_device not in st.session_state.custom_devices:
                st.session_state.custom_devices.append(new_device)
                st.success(f"✅ Added: {new_device}")
            else:
                st.warning(f"⚠️ {new_device} already exists")
        else:
            st.error("Please enter a device name")
    
    if 'custom_devices' in st.session_state and st.session_state.custom_devices:
        st.write("**Configured Devices:**")
        for device in st.session_state.custom_devices:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- {device}")
            with col2:
                if st.button("❌", key=f"remove_{device}"):
                    st.session_state.custom_devices.remove(device)
                    st.rerun()
```

4. **Find the `generate_data()` function and change:**
```python
def generate_data(n=100):
    # Use custom devices if provided
    if 'custom_devices' in st.session_state and st.session_state.custom_devices:
        devices = st.session_state.custom_devices
    else:
        devices = [f"Device_{i}" for i in range(1, 7)]
    
    # Rest stays the same...
```

5. **Restart app and test:**
   - Use the new "Device Configuration" sidebar expander
   - Add custom devices
   - Click "Initialize System" to use your devices

---

## Questions?

Let me know which option you prefer and I can implement it for you!
