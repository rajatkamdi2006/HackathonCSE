import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="HOD Dashboard | FacultyPulse", layout="wide", page_icon="📊")
from ui_utils import apply_custom_css
apply_custom_css()
from auth import check_auth
check_auth()

@st.cache_data
def load_data():
    try:
        return calculate_burnout_risk('faculty_data.csv')
    except FileNotFoundError:
        st.error("Data file missing. Run mock_data.py.")
        st.stop()

df = load_data()

st.title("Welcome, Administrator - CS Dept")
st.markdown("### Workload Intelligence & Early Risk Detection")
st.markdown("---")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
total_faculty = len(df)
avg_workload = round(df['Classes_Per_Week'].mean(), 1)
critical_risk_count = len(df[df['Risk_Status'] == 'Critical'])
warning_count = len(df[df['Risk_Status'] == 'Warning'])

col1.metric("Total Faculty", total_faculty, help="Total number of registered faculty members.")
col2.metric("Avg Classes/Week", avg_workload, help="Average teaching load across the department.")
col3.metric("Critical Risk Faculty", critical_risk_count, help="Faculty highly likely to experience burnout.")
col4.metric("Early Warnings", warning_count, help="Faculty showing signs of elevated stress.")

st.markdown("---")

col_viz, col_insight = st.columns([2, 1])

with col_viz:
    st.subheader("Department Risk Distribution")
    risk_counts = df['Risk_Status'].value_counts()
    st.bar_chart(risk_counts)

with col_insight:
    st.subheader("Action Item: Highest Priority")
    if critical_risk_count > 0:
        highest_risk_faculty = df.loc[df['Burnout_Risk_Score'].idxmax()]
        with st.container():
            st.error(f"🚨 **{highest_risk_faculty['Name']}** \n\n**Risk Score:** {highest_risk_faculty['Burnout_Risk_Score']}")
            st.markdown("This faculty member has the highest workload stress in the department. Please evaluate their workload immediately.")
            if st.button("Manage Workload in Optimization Center", use_container_width=True):
                st.switch_page("pages/3_🔄_Optimization_Center.py")
    else:
        st.success("✅ Department is healthy. No Critical Risk Faculty Detected.")

st.markdown("---")
st.subheader("Faculty Workload Roster")
st.write("Use the interactive filters below to sort, search, and audit your department's workload.")

# Interactive Filters
filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    search_query = st.text_input("🔍 Search by Name", "", help="Type a faculty member's name to filter the table.")
with filter_col2:
    status_filter = st.multiselect("Filter by Risk Status", options=["Optimal", "Warning", "Critical"], default=["Optimal", "Warning", "Critical"])
with filter_col3:
    subject_filter = st.multiselect("Filter by Subject", options=df['Subject_Expertise'].unique(), default=df['Subject_Expertise'].unique())

# Apply filters
filtered_df = df[
    (df['Risk_Status'].isin(status_filter)) & 
    (df['Subject_Expertise'].isin(subject_filter))
]

if search_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False)]

st.dataframe(
    filtered_df[['Faculty_ID', 'Name', 'Subject_Expertise', 'Classes_Per_Week', 'Admin_Hours_Per_Week', 'Max_Consecutive_Classes', 'Burnout_Risk_Score', 'Risk_Status']],
    use_container_width=True,
    hide_index=True
)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Roster to CSV",
    data=csv,
    file_name='faculty_roster_export.csv',
    mime='text/csv',
    help="Download the filtered faculty list for offline administration and reporting."
)
