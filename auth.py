import streamlit as st
import json
import os
import hashlib

USERS_FILE = 'users.json'

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def signup_user(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    
    users[username] = hash_password(password)
    save_users(users)
    return True, "Signup successful! Please switch to the Login tab."

def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.rerun()

def check_auth():
    """To be called at the top of every protected page."""
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("🔒 Unauthorized Access. Please log in from the Main Menu.")
        st.stop()
    else:
        with st.sidebar:
            st.markdown(f"**👤 Logged in as:** {st.session_state['username']}")
            if st.button("Logout"):
                logout()
