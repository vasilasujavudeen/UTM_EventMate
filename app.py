import streamlit as st
import pandas as pd
from datetime import date

# -------------------------
# Load Event Data
# -------------------------
events = pd.read_csv("events.csv")

# -------------------------
# Session State for Login
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
            st.success(f"Welcome, {name}!")
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
        option = st.selectbox(
            "Quick options",
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

        if option == "Faculty Events" and faculty != "All Faculties":
            filtered = filtered[filtered["Faculty"] == faculty]

        if option == "Custom Search":
            filtered = filtered[filtered["Date"] == str(selected_date)]
            if faculty != "All Faculties":
                filtered = filtered[filtered["Faculty"] == faculty]

        # -------------------------
        # OUTPUT EVENTS
        # -------------------------
        if not filtered.empty:
            st.subheader("📌 Matching Events")
            for _, row in filtered.iterrows():
                with st.expander(f"{row['Event']} ({row['Date']})"):
                    st.write(f"🏫 **Faculty:** {row['Faculty']}")
                    st.write(f"📍 **Venue:** {row['Venue']}")
                    st.write(f"🗓 Date: {row['Date']}")
                    st.button("Register Now", key=row["Event"])
        else:
            st.warning("No events found for your selection.")

        # -------------------------
        # Recommended Events (Simulation)
        # -------------------------
        st.subheader("⭐ Recommended for You")
        recommended = events.sample(3)  # Random 3 events
        for _, row in recommended.iterrows():
            st.info(f"{row['Event']} | {row['Date']} | {row['Faculty']}")

    # -------------------------
    # SETTINGS SCREEN
    # -------------------------
    elif page == "Settings":
        st.title("⚙️ Settings")
        st.markdown("**Interests**")
        st.checkbox("Academic Talks")
        st.checkbox("Workshops")
        st.checkbox("Sports & Recreation")
        st.checkbox("Career Events")

        st.markdown("**Notifications**")
        st.checkbox("Enable event reminders")

        st.markdown("**Privacy**")
        st.caption("This prototype does not store personal data.")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()
