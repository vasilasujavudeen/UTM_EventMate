import streamlit as st
import pandas as pd
from datetime import date

# -------------------------
# Load Event Data
# -------------------------
events = pd.read_csv("events.csv")

# -------------------------
# Session State Init
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "registered_events" not in st.session_state:
    st.session_state.registered_events = []
if "recommended_events" not in st.session_state:
    st.session_state.recommended_events = events.sample(3, random_state=1)

# -------------------------
# LOGIN
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
            st.warning("Please enter both fields")

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

        faculty = st.selectbox(
            "Filter by Faculty",
            ["All", "Computing", "Engineering", "Science"]
        )

        selected_date = st.date_input("Select Date", date.today())

        filtered = events.copy()

        if faculty != "All":
            filtered = filtered[filtered["Faculty"] == faculty]

        filtered = filtered[filtered["Date"] >= str(selected_date)]

        st.subheader("📅 Available Events")

        if filtered.empty:
            st.warning("No events found.")
        else:
            for i, row in filtered.iterrows():
                with st.expander(f"{row['Event']} ({row['Date']})"):
                    st.write(f"📂 Category: {row['Category']}")
                    st.write(f"🏫 Faculty: {row['Faculty']}")
                    st.write(f"📍 Venue: {row['Venue']}")

                    if row["Event"] in st.session_state.registered_events:
                        st.success("✅ You are registered")
                    else:
                        if st.button("Register Now", key=f"reg_{i}"):
                            st.session_state.registered_events.append(row["Event"])
                            st.success("🎉 Registration successful")

        # -------------------------
        # RECOMMENDED EVENTS (FIXED)
        # -------------------------
        st.subheader("⭐ Recommended for You")
        for row in st.session_state.recommended_events.itertuples():
            st.info(f"{row.Event} | {row.Date} | {row.Category}")

    # -------------------------
    # EVENT CATEGORIES (FIXED)
    # -------------------------
    elif page == "Event Categories":
        st.title("📂 Event Categories")

        category = st.radio(
            "Choose a category",
            events["Category"].unique()
        )

        cat_events = events[events["Category"] == category]

        st.subheader(f"📌 {category} Events")

        for i, row in cat_events.iterrows():
            with st.expander(f"{row['Event']} ({row['Date']})"):
                st.write(f"🏫 Faculty: {row['Faculty']}")
                st.write(f"📍 Venue: {row['Venue']}")

                if row["Event"] in st.session_state.registered_events:
                    st.success("✅ You are registered")
                else:
                    if st.button("Register Now", key=f"cat_{i}"):
                        st.session_state.registered_events.append(row["Event"])
                        st.success("🎉 Registration successful")

    # -------------------------
    # SETTINGS
    # -------------------------
    elif page == "Settings":
        st.title("⚙️ Settings")

        st.markdown("**Interests**")
        st.multiselect(
            "Select interests",
            ["Academic Talks", "Workshops", "Sports & Recreation", "Career Events", "Cultural Events"]
        )

        st.checkbox("Enable notifications")
        st.checkbox("Enable event reminders")

        st.markdown("**Privacy**")
        st.caption("This prototype does not store personal data.")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.registered_events = []
            st.rerun()
