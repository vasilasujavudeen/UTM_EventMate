
import streamlit as st
import pandas as pd
from datetime import date

# Load event data
events = pd.read_csv("events.csv")

# Sidebar navigation
st.sidebar.title("📌 UTM EventMate")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Chat with EventMate", "Event Categories", "Recommended Events", "Settings"]
)

# -------------------------
# HOME PAGE
# -------------------------
if page == "Home":
    st.title("🏫 UTM EventMate")
    st.markdown("""
    Welcome to **UTM EventMate** – your AI assistant for campus events!

    **Navigation:**
    - Chat with EventMate
    - Event Categories
    - Recommended Events
    - Settings
    """)

# -------------------------
# CHAT WITH EVENTMATE
# -------------------------
elif page == "Chat with EventMate":
    st.title("💬 Chat with EventMate")
    st.write("Ask about campus events or select options below:")

    option = st.selectbox(
        "Search events by:",
        ["Custom Search", "Events Today", "Faculty Events"]
    )

    faculty = st.selectbox(
        "Select Faculty",
        ["All Faculties", "Computing", "Engineering", "Science"]
    )

    selected_date = st.date_input("Select Date", date.today())

    # Filter events
    filtered = events.copy()
    if option == "Events Today":
        filtered = filtered[filtered["Date"] == str(date.today())]

    elif option == "Faculty Events" and faculty != "All Faculties":
        filtered = filtered[filtered["Faculty"] == faculty]

    elif option == "Custom Search":
        filtered = filtered[filtered["Date"] == str(selected_date)]
        if faculty != "All Faculties":
            filtered = filtered[filtered["Faculty"] == faculty]

   # Inside the event loop
if not filtered.empty:
    st.subheader("📌 Matching Events")
    for _, row in filtered.iterrows():
        with st.expander(f"{row['Event']} ({row['Date']})"):
            st.write(f"🏫 **Faculty:** {row['Faculty']}")
            st.write(f"📍 **Venue:** {row['Venue']}")
            st.write(f"🗓 Date: {row['Date']}")

            # Simulate registration
            button_key = f"register_{row['Event']}"
            if st.button("Register Now", key=button_key):
                # Store registration in session state
                if "registrations" not in st.session_state:
                    st.session_state.registrations = []
                if row["Event"] not in st.session_state.registrations:
                    st.session_state.registrations.append(row["Event"])
                    st.success(f"You have successfully registered for **{row['Event']}**!")
                else:
                    st.info(f"You already registered for **{row['Event']}**.")
 # Display results
    if not filtered.empty:
        st.subheader("📌 Matching Events")
        for _, row in filtered.iterrows():
            with st.expander(f"{row['Event']} ({row['Date']})"):
                st.write(f"🏫 **Faculty:** {row['Faculty']}")
                st.write(f"📍 **Venue:** {row['Venue']}")
                st.write(f"🗓 Date: {row['Date']}")

                # Registration simulation
                button_key = f"register_{row['Event']}"
                if st.button("Register Now", key=button_key):
                    if "registrations" not in st.session_state:
                        st.session_state.registrations = []
                    if row["Event"] not in st.session_state.registrations:
                        st.session_state.registrations.append(row["Event"])
                        st.success(f"You have successfully registered for **{row['Event']}**!")
                    else:
                        st.info(f"You already registered for **{row['Event']}**.")
    else:
        st.warning("No events found for your selection.")

    # Show registered events
    if "registrations" in st.session_state and st.session_state.registrations:
        st.subheader("✅ My Registered Events")
        for event in st.session_state.registrations:
            st.info(event)

# -------------------------
# EVENT CATEGORIES
# -------------------------
elif page == "Event Categories":
    st.title("📂 Event Categories")
    categories = ["Academic Talks", "Workshops", "Competitions", "Cultural Events", "Sports & Recreation", "Career Events"]
    for cat in categories:
        cat_events = events[events['Event'].str.contains(cat.split()[0], case=False)]
        st.subheader(cat)
        if not cat_events.empty:
            for _, row in cat_events.iterrows():
                st.write(f"{row['Event']} | {row['Date']} | {row['Faculty']} | {row['Venue']}")
        else:
            st.write("No events found in this category.")

# -------------------------
# RECOMMENDED EVENTS
# -------------------------
elif page == "Recommended Events":
    st.title("⭐ Recommended Events")
    recommended = events.sample(3)
    for _, row in recommended.iterrows():
        st.info(f"{row['Event']} | {row['Date']} | {row['Faculty']} | {row['Venue']}")

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

    st.markdown("**Notifications & Event Reminders**")
    st.checkbox("Enable event reminders")
    st.checkbox("Receive notifications for recommended events")
