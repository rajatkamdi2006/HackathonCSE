import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Shift the sidebar navigation block to the left */
        [data-testid="stSidebarNav"] {
            margin-left: -20px !important;
            padding-left: 0px !important;
        }
        
        /* 2. Force Sidebar background to Black with Yellow Border */
        [data-testid="stSidebar"] {
            background-color: #111111 !important; 
            border-right: 1px solid #FFC107 !important; /* Yellow border line */
        }
        
        /* 3. Force Sidebar text to White initially */
        [data-testid="stSidebarNav"] span {
            color: #FFFFFF !important; 
            font-weight: 500 !important;
        }
        
        /* Hover effect for sidebar items -> Yellow Background, Black text */
        [data-testid="stSidebarNav"] a:hover {
            background-color: #FFC107 !important; 
        }
        [data-testid="stSidebarNav"] a:hover span {
            color: #000000 !important; 
        }
        
        /* Highlight primary active item in yellow */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #222222 !important;
            border-left: 5px solid #FFC107 !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: #FFC107 !important;
        }
        </style>
    """, unsafe_allow_html=True)
