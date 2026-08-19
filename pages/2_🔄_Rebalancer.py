import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="Rebalancer", layout="wide")
st.title("🔄 Workload Rebalancer")

df = calculate_burnout_risk('faculty_data.csv')
critical_df = df[df['Risk_Status'] == 'Critical']

if not critical_df.empty:
    selected_name = st.selectbox("Select Critical Faculty:", options=critical_df['Name'].tolist())
    
    if selected_name:
        target_expertise = df[df['Name'] == selected_name]['Subject_Expertise'].values[0]
        st.write(f"**Target Subject:** {target_expertise}")
        
        substitutes = df[(df['Risk_Status'] == 'Optimal') & (df['Subject_Expertise'] == target_expertise)]
        
        st.subheader("Suggested Substitutes")
        if not substitutes.empty:
            st.dataframe(substitutes[['Name', 'Classes_Per_Week', 'Burnout_Risk_Score']], hide_index=True)
        else:
            st.warning("No 'Optimal' faculty available with this expertise.")
else:
    st.success("No critical faculty to rebalance.")
