import streamlit as st
import pandas as pd
from datetime import date

# -------------------------
# Load Event Data
# -------------------------
events = pd.read_csv("events.csv")

# -------------------------
# Session State
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -------------------------
# LOGIN SCREEN
# -------------------------
if not st.session_state.logged_in:
    st.title("🎓 UTM EventMate")
    st.subheader("Campus Events & Announcements")

    st.write("Please log in to continue")

    name = st.text_input("Name")
    matric = st.text_input("Matric Number")

    if st.button("Login"):
        if name and matric:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.rerun()
        else:
            st.warning("Please enter both name and matric number")

# -------------------------
# MAIN APPLICATION
# -------------------------
else:
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Chat with EventMate", "Settings"]
    )

    # -------------------------
    # HOME SCREEN
    # -------------------------
    if page == "Home":
        st.title("🏫 UTM EventMate")
        st.write(f"Welcome, **{st.session_state.user_name}** 👋")

        st.markdown("""
        **What can EventMate help you with?**
        - 📅 Find upcoming campus events
        - 🎓 Discover faculty-based activities
        - 🔔 Stay updated with announcements
        """)

        st.info("Use the sidebar to start chatting with EventMate.")

    # -------------------------
    # CHAT WITH EVENTMATE
    # -------------------------
    elif page == "Chat with EventMate":
        st.title("💬 Chat with EventMate")

        st.write("Hello! Ask me about campus events 👇")

        # Quick options
        st.markdown("**Quick options:**")
        option = st.selectbox(
            "Choose an option",
            ["Custom Search", "Events Today", "Faculty Events"]
        )

        faculty = st.selectbox(
            "Select Faculty",
            ["All Faculties", "Computing", "Engineering", "Science"]
        )

        selected_date = st.date_input("Select Date", date.today())

        # Filter logic
        filtered = events.copy()

        if option == "Events Today":
            filtered = filtered[filtered["Date"] == str(date.today())]

        if faculty != "All Faculties":
            filtered = filtered[
                (filtered["Faculty"] == faculty) |
                (filtered["Faculty"] == "All Faculties")
            ]

        if option == "Custom Search":
            filtered = filtered[filtered["Date"] == str(selected_date)]

        # -------------------------
        # OUTPUT
        # -------------------------
        if not filtered.empty:
            st.subheader("📌 Matching Events")
            for _, row in filtered.iterrows():
                with st.expander(row["Event"]):
                    st.write(f"📅 **Date:** {row['Date']}")
                    st.write(f"🏫 **Faculty:** {row['Faculty']}")
                    st.write(f"📍 **Venue:** {row['Venue']}")
                    st.button("Register Now", key=row["Event"])
        else:
            st.warning("No events found for your selection.")

    # -------------------------
    # SETTINGS
    # -------------------------
    elif page == "Settings":
        st.title("⚙️ Settings")

        st.markdown("**Interests**")
        st.checkbox("Academic Talks")
        st.checkbox("Workshops")
        st.checkbox("Sports & Recreation")
        st.checkbox("Career Events")

        st.markdown("**Notifications**")
        st.toggle("Enable event reminders")

        st.markdown("**Privacy**")
        st.caption("This prototype does not store personal data.")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()
