import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Health & Gout Tracker", layout="wide")

st.title("🏋️‍♂️ Coach Matt's Health Tracker")
st.subheader("Target Weight: Under 110 kg | Focus: Joint Resilience & Hydration")

# Initialize historical log data directly into the application memory
default_data = [
    {"Date": "2026-06-09", "Weight_kg": 121.1, "Joint_Gout_Status": "Pain-free / Clear", "Cardio_Summary": "Tue: Full Body A"},
    {"Date": "2026-06-06", "Weight_kg": 121.1, "Joint_Gout_Status": "No pain, strict form", "Cardio_Summary": "Sat: Full Body C, Sun: 45 min raking hay"},
    {"Date": "2026-06-04", "Weight_kg": 121.1, "Joint_Gout_Status": "No pain, sweating well, clean eating", "Cardio_Summary": "Thu: Full Body B, Fri: Rest/Mobility"},
    {"Date": "2026-06-02", "Weight_kg": 121.1, "Joint_Gout_Status": "Wrist bump checked - pain-free", "Cardio_Summary": "Tue: Full Body A, Wed: 10000 steps mountain walk"},
    {"Date": "2026-05-30", "Weight_kg": 121.0, "Joint_Gout_Status": "Small gout flare in right wrist (no pain)", "Cardio_Summary": "Sat: Full Body C, Sun: 5000 steps football practice"},
    {"Date": "2026-05-28", "Weight_kg": 121.0, "Joint_Gout_Status": "No pain, sweating well", "Cardio_Summary": "Thu: Full Body B, Fri: Rest/Mobility"},
    {"Date": "2026-05-26", "Weight_kg": 121.0, "Joint_Gout_Status": "Ankles good, slight knee stiffness", "Cardio_Summary": "Tue: Full Body A, Wed: 35-45 min walk"}
]

# Use Streamlit Session State to keep track of entries without needing a local file system
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(default_data)

# Sidebar Form for entry
st.sidebar.header("📝 Log Today's Entry")
entry_date = st.sidebar.date_input("Date", datetime.date.today())
weight = st.sidebar.number_input("Body Weight (kg)", min_value=80.0, max_value=150.0, value=121.1, step=0.1)
gout_status = st.sidebar.selectbox("Joint / Gout Status", ["Pain-free / Clear", "Mild Stiffness / Tingling", "Active Flare"])
activity = st.sidebar.text_area("Workout & Cardio Notes")

if st.sidebar.button("Save Log Entry"):
    new_row = pd.DataFrame([{
        "Date": str(entry_date),
        "Weight_kg": weight,
        "Joint_Gout_Status": gout_status,
        "Cardio_Summary": activity
    }])
    st.session_state.df = pd.concat([new_row, st.session_state.df]).drop_duplicates(subset=["Date"], keep='first').reset_index(drop=True)
    st.sidebar.success("Entry added directly to active log memory!")

# Main Metrics layout
col1, col2 = st.columns(2)
with col1:
    current_w = st.session_state.df["Weight_kg"].dropna().iloc[0] if not st.session_state.df["Weight_kg"].dropna().empty else 121.1
    st.metric(label="Current Weight Baseline", value=f"{current_w} kg")
with col2:
    st.metric(label="Distance to Goal (110 kg)", value=f"{round(current_w - 110.0, 1)} kg left")

# Graph Trend
st.subheader("📈 Weight Loss Runway Tracker")
df_clean = st.session_state.df.dropna(subset=["Weight_kg"]).copy()
if not df_clean.empty:
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    st.line_chart(data=df_clean, x='Date', y='Weight_kg')

# Display Data Table
st.subheader("📅 Log History Database")
st.dataframe(st.session_state.df, use_container_width=True)

# Export Feature for safekeeping
csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download/Export All Data to CSV File", data=csv_data, file_name="health_tracker_data.csv", mime="text/csv")
