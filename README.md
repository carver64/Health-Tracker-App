import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Health Tracker App", layout="wide")

st.title("🏋️‍♂️ Coach Matt's Master Health Dashboard")
st.subheader("Target Weight: Under 110 kg | Frequency: Adaptive Tracking Cadence")

# Unified historical log data schema matching your custom cadence
default_data = [
    {"Date": "2026-06-09", "Weight_kg": 121.1, "Waist_cm": 112.0, "Blood_Pressure": "128/82", "Resting_HR": 68, "Hydration_L": 4.5, "Joint_Gout_Status": "Pain-free / Clear", "Sleep_Quality": "Good", "Cardio_Summary": "Tue: Full Body A"},
    {"Date": "2026-06-06", "Weight_kg": 121.1, "Waist_cm": None, "Blood_Pressure": "126/80", "Resting_HR": 67, "Hydration_L": 4.0, "Joint_Gout_Status": "Pain-free / Clear", "Sleep_Quality": "Excellent", "Cardio_Summary": "Sat: Full Body C, Sun: 45 min raking hay"},
    {"Date": "2026-06-04", "Weight_kg": 121.1, "Waist_cm": None, "Blood_Pressure": None, "Resting_HR": None, "Hydration_L": 4.5, "Joint_Gout_Status": "Pain-free / Clear", "Sleep_Quality": "Good", "Cardio_Summary": "Thu: Full Body B, Fri: Rest/Mobility"},
    {"Date": "2026-06-02", "Weight_kg": 121.1, "Waist_cm": 113.0, "Blood_Pressure": "130/84", "Resting_HR": 70, "Hydration_L": 4.0, "Joint_Gout_Status": "Pain-free / Clear", "Sleep_Quality": "Good", "Cardio_Summary": "Tue: Full Body A, Wed: 10000 steps mountain walk"}
]

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(default_data)

# Sidebar Form - Smart Input based on current day of the week
st.sidebar.header("📝 Log Metrics")
entry_date = st.sidebar.date_input("Date", datetime.date.today())

# Automatically detect if today is a Weekend for the Weekly Pulse Check
is_weekend = entry_date.weekday() in [5, 6] 

st.sidebar.markdown("### 1. Daily Vitals (Every Morning)")
hydration = st.sidebar.number_input("Hydration Intake (Liters)", min_value=0.0, max_value=10.0, value=4.0, step=0.5)
gout_status = st.sidebar.selectbox("Joint / Gout Sensation", ["Pain-free / Clear", "Mild Stiffness / Tingling", "Active Flare"])
sleep_qual = st.sidebar.selectbox("Last Night's Sleep Quality", ["Excellent", "Good", "Fair", "Poor"])
activity = st.sidebar.text_area("Workout & Cardio Notes")

# Show or hide advanced metrics automatically to avoid tracking burnout
if is_weekend:
    st.sidebar.markdown("### 2. Weekend Pulse Check (Fasting)")
    weight = st.sidebar.number_input("Body Weight (kg)", min_value=80.0, max_value=150.0, value=121.1, step=0.1)
    bp = st.sidebar.text_input("Blood Pressure (sys/dia)", value="120/80")
    rhr = st.sidebar.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=120, value=65)
    
    st.sidebar.markdown("### 3. Monthly Progression")
    waist = st.sidebar.number_input("Waist at Belly Button (cm) - Optional", min_value=50.0, max_value=200.0, value=112.0, step=0.5)
else:
    st.sidebar.info("💡 Advanced metrics (Weight, BP, Waist) hide automatically during the week to keep your logging under 60 seconds!")
    weight, waist, bp, rhr = None, None, None, None

if st.sidebar.button("Save Log Entry"):
    new_row = pd.DataFrame([{
        "Date": str(entry_date),
        "Weight_kg": weight,
        "Waist_cm": waist,
        "Blood_Pressure": bp,
        "Resting_HR": rhr,
        "Hydration_L": hydration,
        "Joint_Gout_Status": gout_status,
        "Sleep_Quality": sleep_qual,
        "Cardio_Summary": activity
    }])
    st.session_state.df = pd.concat([new_row, st.session_state.df]).drop_duplicates(subset=["Date"], keep='first').reset_index(drop=True)
    st.sidebar.success("Metrics logged successfully!")

# App Layout Tabs
tab1, tab2, tab3 = st.tabs(["📊 Quick Dashboard", "📅 Full Data Log", "📥 Export Backup"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        latest_w = st.session_state.df["Weight_kg"].dropna().iloc[0] if not st.session_state.df["Weight_kg"].dropna().empty else 121.1
        st.metric(label="Latest Scale Weight", value=f"{latest_w} kg", delta=f"{round(latest_w - 121.1, 1)} kg from start")
    with col2:
        st.metric(label="Distance to Goal (110 kg)", value=f"{round(latest_w - 110.0, 1)} kg left")
    with col3:
        latest_waist = st.session_state.df["Waist_cm"].dropna().iloc[0] if not st.session_state.df["Waist_cm"].dropna().empty else "No entry yet"
        st.metric(label="Waist Circumference", value=f"{latest_waist} cm" if type(latest_waist) == float else latest_waist)

    st.subheader("📈 Local Health Trends")
    df_clean = st.session_state.df.dropna(subset=["Weight_kg"]).copy()
    if not df_clean.empty:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'])
        st.line_chart(data=df_clean, x='Date', y='Weight_kg')

with tab2:
    st.subheader("Complete Health Log History")
    st.dataframe(st.session_state.df, use_container_width=True)

with tab3:
    st.subheader("Data Portability")
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download All Data to CSV File", data=csv_data, file_name="health_tracker_data.csv", mime="text/csv")
