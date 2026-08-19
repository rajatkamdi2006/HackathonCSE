import streamlit as st
from auth import authenticate_user, signup_user, logout

st.set_page_config(page_title="FacultyPulse | Admin Portal", layout="wide", page_icon="🎓")
from ui_utils import apply_custom_css
apply_custom_css()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = None

if not st.session_state['logged_in']:
    st.title("🎓 FacultyPulse - Authentication")
    st.markdown("### Secure Administrator Login")
    st.markdown("---")
    
    # Restrict layout width for the login form to make it look premium
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to your account")
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", type="primary", use_container_width=True):
                if authenticate_user(login_username, login_password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = login_username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
        with tab2:
            st.subheader("Register a new Administrator")
            signup_username = st.text_input("New Username", key="signup_user")
            signup_password = st.text_input("New Password", type="password", key="signup_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            if st.button("Sign Up", use_container_width=True):
                if signup_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(signup_username) < 3 or len(signup_password) < 4:
                    st.error("Username must be >= 3 chars and Password >= 4 chars.")
                else:
                    success, msg = signup_user(signup_username, signup_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
else:
    # Authenticated Portal
    with st.sidebar:
        st.markdown(f"**👤 Logged in as:** {st.session_state['username']}")
        if st.button("Logout"):
            logout()
            
    st.title("🎓 FacultyPulse - Admin Portal")
    st.markdown("### Intelligent Workload & Burnout Management for College Administrators")
    st.markdown("---")

    st.markdown("""
    Welcome to the FacultyPulse administrative portal. This system is designed to help Heads of Departments (HODs) and Deans proactively manage faculty workload, prevent burnout, and optimize class scheduling.

    Please use the sidebar to navigate to the specific modules:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("### 📊 1. Dashboard\nGet a bird's-eye view of your entire department. Monitor KPIs, view the risk distribution, and identify which faculty members require immediate attention.")
        st.info("### 🔄 3. Optimization Center\nTake action on overloaded faculty. Simulate transferring classes to optimal substitutes, or directly grant rest periods to reduce burnout risk.")

    with col2:
        st.info("### 🔍 2. Faculty Detail\nDeep dive into individual faculty profiles. Understand the exact factors (classes, admin hours, consecutive classes) driving their burnout risk score.")
        st.info("### ➕ 4. Add Faculty\nOnboard new faculty members into the department system seamlessly so they are tracked by the risk engine.")
