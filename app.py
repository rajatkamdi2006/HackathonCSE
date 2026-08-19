import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

# Page Config
st.set_page_config(page_title="Faculty Workload & Burnout Analyzer", layout="wide")

st.title("Faculty Workload & Burnout Analyzer")

# Load and process data
@st.cache_data
def load_data():
    try:
        return calculate_burnout_risk('faculty_data.csv')
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Error: 'faculty_data.csv' not found. Please run mock_data.py to generate it first.")
    st.stop()

# --- Top Metrics ---
st.subheader("Dashboard Overview")
col1, col2, col3 = st.columns(3)

total_faculty = len(df)
warning_faculty = len(df[df['Risk_Status'] == 'Warning'])
critical_faculty = len(df[df['Risk_Status'] == 'Critical'])

col1.metric("Total Faculty", total_faculty)
col2.metric("Warning Status", warning_faculty)
col3.metric("Critical Status", critical_faculty)

st.markdown("---")

# --- Visualizations ---
st.subheader("Burnout Risk Score by Faculty")
# Create a bar chart using native Streamlit function
chart_data = df.set_index('Name')['Burnout_Risk_Score']
st.bar_chart(chart_data)

st.subheader("Critical Risk Alert")
critical_df = df[df['Risk_Status'] == 'Critical']

if not critical_df.empty:
    st.error("⚠️ The following faculty members are at Critical risk of burnout:")
    # Display the critical dataframe
    st.dataframe(critical_df, use_container_width=True)
else:
    st.success("✅ No faculty members are currently in Critical status.")

st.markdown("---")

# --- The Innovation Feature: Workload Rebalancer ---
with st.sidebar:
    st.header("Workload Rebalancer")
    st.write("Identify optimal substitutes for critical faculty.")
    
    if not critical_df.empty:
        # Dropdown to select a critical faculty member
        selected_name = st.selectbox(
            "Select Critical Faculty:",
            options=critical_df['Name'].tolist()
        )
        
        if selected_name:
            # Retrieve expertise of the selected faculty
            target_expertise = df[df['Name'] == selected_name]['Subject_Expertise'].values[0]
            st.write(f"**Target Subject:** {target_expertise}")
            
            # Find optimal faculty with matching expertise
            substitutes = df[
                (df['Risk_Status'] == 'Optimal') & 
                (df['Subject_Expertise'] == target_expertise)
            ]
            
            st.subheader("Suggested Substitutes")
            if not substitutes.empty:
                st.success("Found suitable rebalance options:")
                # Show only relevant columns for substitutes
                st.dataframe(
                    substitutes[['Name', 'Classes_Per_Week', 'Burnout_Risk_Score']], 
                    hide_index=True
                )
            else:
                st.warning("No 'Optimal' faculty available with this expertise.")
    else:
        st.info("No critical faculty to rebalance.")
