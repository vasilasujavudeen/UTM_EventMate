import streamlit as st
import pandas as pd

# Load events
events = pd.read_csv('events.csv')

st.title("UTM EventMate: Campus Event Chatbot")
st.write("Welcome! Ask about upcoming campus events.")

# User input
faculty = st.selectbox("Select Faculty", options=['All', 'Computing', 'Engineering', 'Science', 'All Faculties'])
date_input = st.date_input("Choose Date")

# Filter events
filtered = events.copy()
if faculty != 'All':
    filtered = filtered[(filtered['Faculty'] == faculty) | (filtered['Faculty'] == 'All Faculties')]
filtered = filtered[filtered['Date'] == str(date_input)]

# Display results
if not filtered.empty:
    st.subheader("Recommended Events:")
    for i, row in filtered.iterrows():
        st.write(f"**{row['Event']}** - {row['Venue']} - {row['Faculty']}")
else:
    st.write("No events found for your selection.")
