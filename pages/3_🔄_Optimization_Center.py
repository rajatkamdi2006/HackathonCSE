import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="Optimization Center | FacultyPulse", layout="wide", page_icon="🔄")
from ui_utils import apply_custom_css
apply_custom_css()
from auth import check_auth
check_auth()

@st.cache_data
def load_data():
    return calculate_burnout_risk('faculty_data.csv')

df = load_data()

st.title("🔄 Administration Optimization Center")
st.markdown("Safely rebalance the department's workload dynamically, grant rest periods, and resolve critical bottlenecks.")
st.markdown("---")

with st.expander("ℹ️ How does the simulator work?"):
    st.write("""
    The What-If Simulator allows administrators to preview the impact of timetable changes before making them official. 
    It recalculates the Risk Score in real-time based on the engine's formula:
    `Risk = (1.5 * Classes) + (1.0 * Admin) + Consecutive Penalty + (Complexity * 5)`
    """)

# HOD needs to see overloaded faculty
st.subheader("Overloaded Faculty Pipeline")
overloaded_df = df[df['Risk_Status'].isin(['Critical', 'Warning'])]

if overloaded_df.empty:
    st.success("✅ No overloaded faculty detected. The department workload is perfectly balanced!")
    st.stop()

selected_name = st.selectbox("1. Select Overloaded Faculty Member to Resolve:", overloaded_df['Name'].tolist(), help="This list only shows faculty in Warning or Critical status.")
faculty_data = overloaded_df[overloaded_df['Name'] == selected_name].iloc[0]

st.error(f"**Target Faculty:** {faculty_data['Name']} | **Current Risk Score:** {faculty_data['Burnout_Risk_Score']} ({faculty_data['Risk_Status']})")
st.write(f"**Subject Expertise:** {faculty_data['Subject_Expertise']} | **Current Teaching Load:** {faculty_data['Classes_Per_Week']} Classes/Week")
st.markdown("---")

st.subheader("2. Choose Resolution Strategy")
tab1, tab2 = st.tabs(["🔄 Strategy A: Transfer Workload to Substitute", "🛋️ Strategy B: Direct Adjustment (Provide Rest)"])

with tab1:
    col_sub, col_sim = st.columns([1, 1])
    
    with col_sub:
        st.markdown("#### Available Substitutes (Optimal Status)")
        substitutes = df[(df['Risk_Status'] == 'Optimal') & (df['Subject_Expertise'] == faculty_data['Subject_Expertise'])]
        
        if substitutes.empty:
            st.warning("No optimal substitutes available in this subject area to absorb the workload.")
            substitute_name = None
        else:
            substitute_name = st.selectbox("Select Substitute Faculty:", substitutes['Name'].tolist(), key='sub_select')
            sub_data = substitutes[substitutes['Name'] == substitute_name].iloc[0]
            st.success(f"**{sub_data['Name']}** is available. (Current Risk Score: {sub_data['Burnout_Risk_Score']})")

    with col_sim:
        st.markdown("#### Transfer Simulator")
        if substitutes.empty:
            st.info("Simulation unavailable without substitutes. Try Strategy B instead.")
        else:
            classes_to_transfer = st.slider("Classes to Transfer to Substitute", min_value=1, max_value=10, value=2, step=1, key='transfer_slider', help="Slide to preview how transferring classes impacts both faculty members.")
            
            # Recalculate Logic
            new_classes = max(0, faculty_data['Classes_Per_Week'] - classes_to_transfer)
            base_class_score = 1.5 * new_classes
            base_admin_score = 1.0 * faculty_data['Admin_Hours_Per_Week']
            consec_penalty = 20 if faculty_data['Max_Consecutive_Classes'] >= 3 else 0
            comp_weight = faculty_data['Subject_Complexity_Multiplier'] * 5
            
            new_score_raw = base_class_score + base_admin_score + consec_penalty + comp_weight
            new_score = round(min(100.0, new_score_raw), 2)
            score_delta = round(new_score - faculty_data['Burnout_Risk_Score'], 2)
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label=f"Projected Score: {faculty_data['Name']}", value=new_score, delta=score_delta, delta_color="inverse")
            with m2:
                sub_new_classes = sub_data['Classes_Per_Week'] + classes_to_transfer
                s_base_class = 1.5 * sub_new_classes
                s_base_admin = 1.0 * sub_data['Admin_Hours_Per_Week']
                s_consec_penalty = 20 if sub_data['Max_Consecutive_Classes'] >= 3 else 0
                s_comp_weight = sub_data['Subject_Complexity_Multiplier'] * 5
                
                sub_new_score_raw = s_base_class + s_base_admin + s_consec_penalty + s_comp_weight
                sub_new_score = round(min(100.0, sub_new_score_raw), 2)
                sub_score_delta = round(sub_new_score - sub_data['Burnout_Risk_Score'], 2)
                st.metric(label=f"Projected Score: {sub_data['Name']}", value=sub_new_score, delta=sub_score_delta, delta_color="inverse")
                
            if st.button("Confirm & Apply Transfer", type="primary", help="This will permanently update the department database."):
                raw_df = pd.read_csv('faculty_data.csv')
                raw_df.loc[raw_df['Name'] == faculty_data['Name'], 'Classes_Per_Week'] -= classes_to_transfer
                raw_df.loc[raw_df['Name'] == substitute_name, 'Classes_Per_Week'] += classes_to_transfer
                raw_df.to_csv('faculty_data.csv', index=False)
                
                st.cache_data.clear()
                st.toast("Workload successfully redistributed!")
                st.balloons()
                st.rerun()

with tab2:
    st.markdown("#### Direct Workload Adjustment")
    st.write("If no substitute is available, manually reduce teaching or administrative hours to provide immediate relief.")
    
    col_adj, col_sim2 = st.columns([1, 1])
    with col_adj:
        new_classes_val = st.number_input("Adjust Classes Per Week", min_value=0, max_value=int(faculty_data['Classes_Per_Week']), value=int(faculty_data['Classes_Per_Week']), step=1, help="Reduce this number to simulate dropping a class.")
        new_admin_val = st.number_input("Adjust Admin Hours Per Week", min_value=0, max_value=int(faculty_data['Admin_Hours_Per_Week']), value=int(faculty_data['Admin_Hours_Per_Week']), step=1, help="Reduce this number to relieve them of administrative duties.")
        new_consec_val = st.number_input("Adjust Max Consecutive Classes", min_value=1, max_value=int(faculty_data['Max_Consecutive_Classes']), value=int(faculty_data['Max_Consecutive_Classes']), step=1, help="Fix their timetable to ensure they don't have 3+ consecutive classes.")
        
    with col_sim2:
        st.markdown("#### Live Impact Preview")
        base_class_score2 = 1.5 * new_classes_val
        base_admin_score2 = 1.0 * new_admin_val
        consec_penalty2 = 20 if new_consec_val >= 3 else 0
        comp_weight2 = faculty_data['Subject_Complexity_Multiplier'] * 5
        
        new_score_raw2 = base_class_score2 + base_admin_score2 + consec_penalty2 + comp_weight2
        new_score2 = round(min(100.0, new_score_raw2), 2)
        score_delta2 = round(new_score2 - faculty_data['Burnout_Risk_Score'], 2)
        
        st.metric(label="Projected Risk Score", value=new_score2, delta=score_delta2, delta_color="inverse")
        
        if st.button("Save Rest Periods to Database", type="primary", help="Commits these hour reductions to the faculty roster."):
            raw_df = pd.read_csv('faculty_data.csv')
            raw_df.loc[raw_df['Name'] == faculty_data['Name'], 'Classes_Per_Week'] = new_classes_val
            raw_df.loc[raw_df['Name'] == faculty_data['Name'], 'Admin_Hours_Per_Week'] = new_admin_val
            raw_df.loc[raw_df['Name'] == faculty_data['Name'], 'Max_Consecutive_Classes'] = new_consec_val
            raw_df.to_csv('faculty_data.csv', index=False)
            
            st.cache_data.clear()
            st.toast(f"Rest periods successfully applied for {faculty_data['Name']}!")
            st.success("Adjustment Saved Successfully!")
            st.balloons()
            st.rerun()
