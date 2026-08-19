import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="Faculty Detail | FacultyPulse", layout="wide", page_icon="🔍")
from ui_utils import apply_custom_css
apply_custom_css()
from auth import check_auth
check_auth()

@st.cache_data
def load_data():
    return calculate_burnout_risk('faculty_data.csv')

df = load_data()

with st.sidebar:
    st.header("Select Faculty")
    selected_name = st.selectbox("Search / Select Faculty Member", df['Name'].tolist())
    st.info("Use this page to audit individual faculty profiles and understand the specific drivers behind their burnout score.")

faculty_data = df[df['Name'] == selected_name].iloc[0]

st.title(f"Profile: {faculty_data['Name']}")
st.markdown(f"**Department:** Computer Science | **Subject Expertise:** {faculty_data['Subject_Expertise']} | **Employee ID:** {faculty_data['Faculty_ID']}")
st.markdown("---")

# Profile Header
col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Overall Burnout Risk Score", faculty_data['Burnout_Risk_Score'], help="Scale: 0-100. Over 75 is Critical.")
    if faculty_data['Risk_Status'] == 'Critical':
        st.error("Status: CRITICAL (Immediate Intervention Required)")
    elif faculty_data['Risk_Status'] == 'Warning':
        st.warning("Status: WARNING (Monitor Closely)")
    else:
        st.success("Status: OPTIMAL (Healthy Workload)")
        
    st.markdown("### Quick Actions")
    if st.button("Optimize Workload for this Faculty"):
        st.switch_page("pages/3_🔄_Optimization_Center.py")

with col2:
    st.subheader("Explainable Risk Breakdown")
    st.write("Understand the key drivers behind the burnout risk score. A full progress bar indicates maximum stress for that category.")
    
    st.markdown(f"**Teaching Load:** {faculty_data['Classes_Per_Week']} Classes/Week")
    classes_pct = min(faculty_data['Classes_Per_Week'] / 25.0, 1.0)
    st.progress(classes_pct)
    
    st.markdown(f"**Administrative Load:** {faculty_data['Admin_Hours_Per_Week']} Hours/Week")
    admin_pct = min(faculty_data['Admin_Hours_Per_Week'] / 15.0, 1.0)
    st.progress(admin_pct)
    
    st.markdown(f"**Max Consecutive Classes:** {faculty_data['Max_Consecutive_Classes']}")
    if faculty_data['Max_Consecutive_Classes'] > 2:
        st.error("⚠️ Heavy Penalty Applied: Consecutive classes exceed optimal threshold of 2. This causes severe fatigue.")
    else:
        st.success("✅ Within optimal consecutive bounds (≤ 2).")
        
    st.markdown(f"**Subject Complexity Multiplier:** {faculty_data['Subject_Complexity_Multiplier']}x")
    complexity_pct = min((faculty_data['Subject_Complexity_Multiplier'] - 1.0) / 0.5, 1.0)
    st.progress(complexity_pct)
