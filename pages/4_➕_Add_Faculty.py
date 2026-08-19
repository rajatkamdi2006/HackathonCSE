import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="Add Faculty | FacultyPulse", layout="wide", page_icon="➕")
from ui_utils import apply_custom_css
apply_custom_css()
from auth import check_auth
check_auth()

st.title("➕ Administrative Portal: Add Faculty")
st.markdown("Register a new faculty member into the department roster. Their initial workload will immediately be processed by the risk engine.")
st.markdown("---")

@st.cache_data
def load_data():
    return calculate_burnout_risk('faculty_data.csv')

df = load_data()

with st.form("add_faculty_form"):
    st.subheader("Faculty Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", help="Enter the official name of the faculty member.")
        subject = st.selectbox("Primary Subject Expertise", df['Subject_Expertise'].unique().tolist() + ["Other"], help="The main subject area they are contracted to teach.")
        if subject == "Other":
            subject = st.text_input("Specify New Subject")
        
        complexity = st.number_input("Subject Complexity Multiplier", min_value=1.0, max_value=2.0, value=1.2, step=0.1, help="1.0 for basic subjects, up to 2.0 for highly advanced/grading-heavy subjects.")
    
    with col2:
        classes = st.number_input("Initial Classes Per Week", min_value=0, max_value=40, value=15, step=1, help="Total teaching hours assigned per week.")
        admin = st.number_input("Initial Admin Hours Per Week", min_value=0, max_value=20, value=5, step=1, help="Total hours dedicated to administrative/committee duties.")
        consecutive = st.number_input("Max Consecutive Classes on Timetable", min_value=1, max_value=6, value=2, step=1, help="Warning: 3 or more triggers a severe burnout penalty.")
        
    st.markdown("---")
    submit = st.form_submit_button("Create Faculty Record", type="primary")

if submit:
    if not name:
        st.error("Please enter the faculty's name.")
    elif not subject:
        st.error("Please specify their subject expertise.")
    else:
        new_id = int(df['Faculty_ID'].max() + 1) if not df.empty else 1000
        new_row = {
            'Faculty_ID': new_id,
            'Name': name,
            'Subject_Expertise': subject,
            'Subject_Complexity_Multiplier': complexity,
            'Classes_Per_Week': classes,
            'Admin_Hours_Per_Week': admin,
            'Max_Consecutive_Classes': consecutive
        }
        
        raw_df = pd.read_csv('faculty_data.csv')
        raw_df = pd.concat([raw_df, pd.DataFrame([new_row])], ignore_index=True)
        raw_df.to_csv('faculty_data.csv', index=False)
        
        st.cache_data.clear()
        st.success(f"✅ Record created! {name} (ID: {new_id}) has been added to the department roster.")
        st.balloons()
