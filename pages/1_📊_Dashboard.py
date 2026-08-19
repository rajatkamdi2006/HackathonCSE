import streamlit as st
import pandas as pd
from engine import calculate_burnout_risk

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Faculty Workload Dashboard")

df = calculate_burnout_risk('faculty_data.csv')

# --- Top Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Faculty", len(df))
col2.metric("Warning Status", len(df[df['Risk_Status'] == 'Warning']))
col3.metric("Critical Status", len(df[df['Risk_Status'] == 'Critical']))

st.markdown("---")

# --- Visualizations ---
st.subheader("Burnout Risk Score by Faculty")
st.bar_chart(df.set_index('Name')['Burnout_Risk_Score'])
