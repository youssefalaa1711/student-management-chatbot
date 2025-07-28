import streamlit as st
import json
import os

st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# ---- File Paths ----
CREDENTIALS_FILE = "credentials.json"  # Admin
USERS_FILE = "users.json"              # Registered users

# ---- Load or Initialize JSON Data ----
def load_json(file_path, default={}):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(default, f)
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ---- Main Login App ----
def login_system():
    st.title("🔐 Login or Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---- Login Tab ----
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.radio("Login as:", ["User", "Admin"])
        login_btn = st.button("Login")

        if login_btn:
            if role == "Admin":
                credentials = load_json(CREDENTIALS_FILE)
                if credentials.get(username) == password:
                    st.session_state.username = username
                    st.session_state.role = "admin"
                    st.success("Logged in as Admin")
                    st.switch_page("pages/app.py") 
                else:
                    st.error("Invalid Admin credentials.")
            else:
                users = load_json(USERS_FILE)
                if users.get(username) == password:
                    st.session_state.username = username
                    st.session_state.role = "user"
                    st.success("Logged in as User")
                    st.switch_page("app.py")
                else:
                    st.error("Invalid User credentials.")

    # ---- Register Tab ----
    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_btn = st.button("Register")

        if register_btn:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(new_password) < 4:
                st.warning("Password too short (min 4 characters).")
            else:
                users = load_json(USERS_FILE)
                if new_username in users:
                    st.warning("Username already exists.")
                else:
                    users[new_username] = new_password
                    save_json(USERS_FILE, users)
                    st.success("Registration successful. You can now log in.")

# ---- Run App ----
if __name__ == "__main__":
    login_system()
