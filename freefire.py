import streamlit as st
import pandas as pd
import os

# Store registrations, match data, and chat messages
registrations = []
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}
hosting_members = []
notices = []  # List to store notices
player_photos = {}  # Dictionary to store player ID photos
chat_messages = []  # Chat messages for Connections
match_schedule = []  # List to store match schedule

# Define house logos
house_logos = {
    "Aravali": "Arv.png",
    "Nilgiri": "Nil.png",
    "Shiwalik": "Shiw.jpeg",
    "Udaygiri": "Udi.jpeg"
}

# Points table for tracking scores
point_table = pd.DataFrame({
    "House": ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"],
    "Wins": [0, 0, 0, 0],
    "Losses": [0, 0, 0, 0],
    "Points": [0, 0, 0, 0]
})

# Directory to store uploaded images and CSV
UPLOAD_DIR = "uploaded_photos"
ID_PHOTOS_DIR = "id_photos"
REGISTRATION_CSV = "registrations.csv"

# Ensure the upload directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ID_PHOTOS_DIR, exist_ok=True)

# Ensure the CSV files exist
if not os.path.exists(REGISTRATION_CSV):
    pd.DataFrame(columns=["Name", "Class", "House", "Free Fire UID"]).to_csv(REGISTRATION_CSV, index=False)

# Load CSV data functions
def load_csv_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# Save CSV data functions
def save_csv_data(df, file_path):
    df.to_csv(file_path, index=False)

# Admin password for owner access
ADMIN_PASSWORD = "linkan737"  # Updated owner password

# Streamlit app starts here
st.title("Free Fire League")

# Add a sidebar to navigate between pages
page = st.sidebar.selectbox("Select a page", [
    "Registration",
    "Host Registration",
    "Team Info",
    "Schedule",
    "Point Table",
    "Player Stats",
    "Highlights",
    "Pictures",
    "Payment",
    "Connections",
    "Notices",
    "Rules"
])

# Load the registration DataFrame from CSV
registration_df = load_csv_data(REGISTRATION_CSV)

if page == "Point Table":
    st.header("Point Table")
    # Increase the size of the point table for better visibility
    st.dataframe(point_table.style.set_properties(**{'font-size': '16pt'}))

elif page == "Notices":
    st.header("Notices")

    # Display existing notices for everyone
    if notices:
        st.write("### Existing Notices")
        for notice in notices:
            st.write(f"- {notice}")

    # Owner password input for adding notices
    password = st.text_input("Enter Admin Password to Add Notices", type="password")
    if password == ADMIN_PASSWORD:
        notice_input = st.text_area("Add a Notice")
        if st.button("Submit Notice"):
            if notice_input:
                notices.append(notice_input)
                st.success("Notice added!")
            else:
                st.error("Please enter a notice.")

elif page == "Rules":
    st.header("Rules")
    
    # Display existing rules for everyone
    if notices:  # Use notices list to display rules
        st.write("### Existing Rules")
        for rule in notices:
            st.write(f"- {rule}")
    
    # Owner password input for adding rules
    password = st.text_input("Enter Admin Password to Add Rules", type="password")
    if password == ADMIN_PASSWORD:
        rule_input = st.text_area("Add a Rule")
        if st.button("Submit Rule"):
            if rule_input:
                notices.append(rule_input)  # Use notices list to store rules too
                st.success("Rule added!")
            else:
                st.error("Please enter a rule.")

elif page == "Connections":
    st.header("Connections")

    # Simple chat system (available for everyone)
    chat_message = st.text_input("Type your message")
    if st.button("Send"):
        if chat_message:
            chat_messages.append(chat_message)
            st.experimental_rerun()  # Use rerun to show updated chat messages
        else:
            st.error("Message cannot be empty!")

    # Display chat messages
    if chat_messages:
        st.write("### Chat Messages")
        for message in chat_messages:
            st.write(message)

# Add a Twitter follow link at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("Follow me on [Twitter @SwapnilaSwayam](https://twitter.com/SwapnilaSwayam)")
