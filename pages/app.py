import streamlit as st
from chatbot import Chatbot
from database import Database
import pandas as pd

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .big-table-container {
        width: 100% !important;
        min-width: 800px !important;
        margin-left: -40px;  /* Optional: shift left to use more space */
    }
    .big-table-container table {
        width: 100% !important;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize chatbot and session ---
if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot(Database())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chatbot = st.session_state.chatbot

# --- Page Title ---
st.title("🎓 Student Assistant Chatbot")

# --- Sidebar: Quick Actions ---
st.sidebar.header("📚 Quick Actions")

if st.sidebar.button("Add Student"):
    response = chatbot.ask("add student")
    st.session_state.chat_history.append(("user", "add student"))
    st.session_state.chat_history.append(("bot", response))

if st.sidebar.button("Fetch Students"):
    response = chatbot.ask("fetch students")
    st.session_state.chat_history.append(("user", "fetch students"))
    st.session_state.chat_history.append(("bot", response))

if st.sidebar.button("Delete Student"):
    response = chatbot.ask("delete student")
    st.session_state.chat_history.append(("user", "delete student"))
    st.session_state.chat_history.append(("bot", response))

if st.sidebar.button("Update Student"):
    response = chatbot.ask("update student")
    st.session_state.chat_history.append(("user", "update student"))
    st.session_state.chat_history.append(("bot", response))

st.sidebar.markdown("---")

if st.sidebar.button("Reset Chat"):
    chatbot.reset_session()
    st.session_state.chat_history = []

# --- Sidebar: Settings ---
st.sidebar.markdown("### ⚙️ Settings")
bubble_color = st.sidebar.color_picker("Choose your chat bubble color:", "#DCF8C6")
st.session_state["user_bubble_color"] = bubble_color

# --- Sidebar: Logout Button (light red color) ---
logout_btn = st.sidebar.button("Logout", key="logout_btn")

if logout_btn:
    for key in ["username", "role", "chatbot", "chat_history"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Logged out!")
    st.switch_page("login.py")

# Custom CSS for light red logout button
st.markdown("""
    <style>
    [data-testid="stSidebar"] button[kind="secondary"][key="logout_btn"] {
        background-color: #ffcccc !important;
        color: #a94442 !important;
        border: 1px solid #a94442 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Chat Interface ---
user_input = st.chat_input("Type your message...")

if user_input:
    response = chatbot.ask(user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", response))

# --- Display Chat History with Alignment ---
for sender, msg in st.session_state.chat_history:
    is_user = sender == "user"
    col1, col2 = st.columns([1, 1])

    if is_user:
        with col2:
            color = st.session_state.get("user_bubble_color", "#DCF8C6")
            st.markdown(
                f"<div style='text-align:right; background-color:{color}; padding:8px; "
                f"border-radius:8px; margin:5px;'><strong>You:</strong><br>{msg}</div>",
                unsafe_allow_html=True
            )
    else:
        with col1:
            mode = st.get_option("theme.base")  # 'dark' or 'light'
            bot_bubble_color = "#333333" if mode == "dark" else "#F1F0F0"
            text_color = "#FFFFFF" if mode == "dark" else "#000000"

            # Try formatting student list as table
            if ": " in msg and "Grade:" in msg and "\n" in msg:
                rows = msg.strip().split("\n")
                data = []
                for row in rows:
                    try:
                        parts = row.split(":")
                        student_id = parts[0].strip()
                        details = ":".join(parts[1:]).split(",")
                        name = details[0].strip()
                        age = details[1].split(":")[1].strip()
                        grade = details[2].split(":")[1].strip()
                        data.append({
                            "ID": student_id,
                            "Name": name,
                            "Age": age,
                            "Grade": grade
                        })
                    except:
                        data = None
                        break
                if data:
                    st.markdown(f"<div style='color:{text_color};'><strong>Bot:</strong></div>", unsafe_allow_html=True)
                    df = pd.DataFrame(data)
                    st.markdown(
                        f'<div class="big-table-container">{df.to_html(index=False)}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div style='text-align:left; background-color:{bot_bubble_color}; color:{text_color}; "
                        f"padding:8px; border-radius:8px; margin:5px;'><strong>Bot:</strong><br>{msg}</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    f"<div style='text-align:left; background-color:{bot_bubble_color}; color:{text_color}; "
                    f"padding:8px; border-radius:8px; margin:5px;'><strong>Bot:</strong><br>{msg}</div>",
                    unsafe_allow_html=True
                )
