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
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# -------------------------
# LOGIN SCREEN
# -------------------------
if not st.session_state.logged_in:
    st.title("🎓 UTM EventMate")
    st.subheader("Campus Events & Announcements")

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
# MAIN APP
# -------------------------
else:
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Chat with EventMate", "Event Categories", "Settings"]
    )

    # -------------------------
    # HOME
    # -------------------------
    if page == "Home":
        st.title("🏫 UTM EventMate")
        st.write(f"Welcome, **{st.session_state.user_name}** 👋")

        st.markdown("""
        **Available Features**
        - 💬 Chat with EventMate
        - 📂 Browse Event Categories
        - ⭐ View Recommended Events
        - ⚙️ Customize Settings
        """)

    # -------------------------
    # CHAT WITH EVENTMATE
    # -------------------------
    elif page == "Chat with EventMate":
        st.title("💬 Chat with EventMate")

        option = st.selectbox(
            "Quick Search",
            ["Custom Search", "Events Today", "Faculty Events"]
        )

        faculty = st.selectbox(
            "Select Faculty",
            ["All Faculties", "Computing", "Engineering", "Science"]
        )

        selected_date = st.date_input("Select Date", date.today())

        filtered = events.copy()

        if option == "Events Today":
            filtered = filtered[filtered["Date"] == str(date.today())]

        if option == "Faculty Events" and faculty != "All Faculties":
            filtered = filtered[filtered["Faculty"] == faculty]

        if option == "Custom Search":
            filtered = filtered[filtered["Date"] == str(selected_date)]
            if faculty != "All Faculties":
                filtered = filtered[filtered["Faculty"] == faculty]

        if not filtered.empty:
            st.subheader("📅 Matching Events")
            for i, row in filtered.iterrows():
                with st.expander(f"{row['Event']} ({row['Date']})"):
                    st.write(f"📂 Category: {row['Category']}")
                    st.write(f"🏫 Faculty: {row['Faculty']}")
                    st.write(f"📍 Venue: {row['Venue']}")
                    if st.button("Register Now", key=f"reg{i}"):
                        st.success("✅ Registered successfully (simulation)")
        else:
            st.warning("No events found.")

        # Recommended Events
        st.subheader("⭐ Recommended for You")
        for _, row in events.sample(3).iterrows():
            st.info(f"{row['Event']} | {row['Date']} | {row['Category']}")

    # -------------------------
    # EVENT CATEGORIES (NEW)
    # -------------------------
    elif page == "Event Categories":
        st.title("📂 Event Categories")
        st.write("Select a category to view events")

        categories = events["Category"].unique()

        for cat in categories:
            if st.button(cat):
                st.session_state.selected_category = cat

        if st.session_state.selected_category:
            st.subheader(f"📌 {st.session_state.selected_category} Events")

            cat_events = events[
                events["Category"] == st.session_state.selected_category
            ]

            for i, row in cat_events.iterrows():
                with st.expander(f"{row['Event']} ({row['Date']})"):
                    st.write(f"🏫 Faculty: {row['Faculty']}")
                    st.write(f"📍 Venue: {row['Venue']}")
                    if st.button("Register Now", key=f"cat{i}"):
                        st.success("✅ Registered successfully (simulation)")

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
        st.checkbox("Cultural Events")

        st.markdown("**Notifications**")
        st.checkbox("Enable event reminders")

        st.markdown("**Privacy**")
        st.caption("No personal data is stored in this prototype.")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()


