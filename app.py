import streamlit as st
import pandas as pd
from datetime import date

# -------------------------
# Load Event Data
# -------------------------
events = pd.read_csv("events.csv")  # Make sure you have a 'Category' column

# -------------------------
# Session State
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "registered_events" not in st.session_state:
    st.session_state.registered_events = []
if "recommended_events" not in st.session_state:
    st.session_state.recommended_events = events.sample(3, random_state=1)  # Stable recommended

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
# MAIN APPLICATION
# -------------------------
else:
    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Chat with EventMate", "Event Categories", "Settings"]
    )

    # -------------------------
    # HOME SCREEN
    # -------------------------
    if page == "Home":
        st.title("🏫 UTM EventMate")
        st.write(f"Welcome, **{st.session_state.user_name}** 👋")
        st.markdown("""
        **What can EventMate help you with?**
        - 💬 Chat with EventMate
        - 📂 Browse Event Categories
        - ⭐ View Recommended Events
        - ⚙️ Personalize Settings
        """)

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

        # Output Events
        if not filtered.empty:
            st.subheader("📌 Matching Events")
            for i, row in filtered.iterrows():
                with st.expander(f"{row['Event']} ({row['Date']})"):
                    st.write(f"📂 Category: {row['Category']}")
                    st.write(f"🏫 Faculty: {row['Faculty']}")
                    st.write(f"📍 Venue: {row['Venue']}")

                    # Register button
                    if row["Event"] in st.session_state.registered_events:
                        st.success("✅ You are registered")
                    else:
                        if st.button("Register Now", key=f"chat_reg_{i}"):
                            st.session_state.registered_events.append(row["Event"])
                            st.success("🎉 Registration successful")
        else:
            st.warning("No events found for your selection.")

        # Recommended Events
        st.subheader("⭐ Recommended for You")
        for row in st.session_state.recommended_events.itertuples():
            st.info(f"{row.Event} | {row.Date} | {row.Category}")

    # -------------------------
    # EVENT CATEGORIES
    # -------------------------
    elif page == "Event Categories":
        st.title("📂 Event Categories")
        st.write("Select a category to view events")

        categories = events["Category"].unique()
        category = st.radio("Choose Category", categories)

        cat_events = events[events["Category"] == category]

        st.subheader(f"📌 {category} Events")
        for i, row in cat_events.iterrows():
            with st.expander(f"{row['Event']} ({row['Date']})"):
                st.write(f"🏫 Faculty: {row['Faculty']}")
                st.write(f"📍 Venue: {row['Venue']}")

                if row["Event"] in st.session_state.registered_events:
                    st.success("✅ You are registered")
                else:
                    if st.button("Register Now", key=f"cat_reg_{i}"):
                        st.session_state.registered_events.append(row["Event"])
                        st.success("🎉 Registration successful")

    # -------------------------
    # SETTINGS SCREEN
    # -------------------------
    elif page == "Settings":
        st.title("⚙️ Settings")
        st.markdown("**Interests**")
        st.multiselect(
            "Select interests",
            ["Academic Talks", "Workshops", "Sports & Recreation", "Career Events", "Cultural Events"]
        )

        st.markdown("**Notifications**")
        st.checkbox("Enable event reminders")

        st.markdown("**Privacy**")
        st.caption("This prototype does not store personal data.")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.registered_events = []
            st.rerun()
