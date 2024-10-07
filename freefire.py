import streamlit as st
import pandas as pd
import os

# Directory to store uploaded images and CSV
UPLOAD_DIR = "uploaded_photos"
ID_PHOTOS_DIR = "id_photos"
REGISTRATION_CSV = "registrations.csv"

# Ensure the upload directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ID_PHOTOS_DIR, exist_ok=True)

# Admin password for owner access
ADMIN_PASSWORD = "linkan737"  # Updated owner password

# Load CSV data functions
def load_csv_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame(columns=["Name", "Class", "House", "Free Fire UID"])

# Save CSV data functions
def save_csv_data(df, file_path):
    df.to_csv(file_path, index=False)

# Initialize session state for various features
if "notices" not in st.session_state:
    st.session_state.notices = []
if "rules" not in st.session_state:
    st.session_state.rules = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "match_schedule" not in st.session_state:
    st.session_state.match_schedule = []
if "player_photos" not in st.session_state:
    st.session_state.player_photos = {}  # Initialize player photos dictionary

# Load the registration DataFrame from CSV
registration_df = load_csv_data(REGISTRATION_CSV)

# Define house logos (can add actual images)
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

if page == "Team Info":
    st.header("Team Information")
    
    # Display team information based on house registrations
    if not registration_df.empty:
        for house in house_logos.keys():
            st.write(f"### {house}")
            st.image(house_logos[house], width=100)  # Display the house logo
            team_players = registration_df[registration_df["House"] == house]
            if not team_players.empty:
                for idx, player in team_players.iterrows():
                    st.write(f"**{player['Name']}** (Class: {player['Class']}, Free Fire UID: {player['Free Fire UID']})")
                    # Display the player photo if available
                    photo_path = st.session_state.player_photos.get(player["Free Fire UID"])
                    if photo_path and os.path.exists(photo_path):
                        st.image(photo_path, width=100)
                    else:
                        st.write("No photo available.")
            else:
                st.write(f"No players registered for {house} yet.")
    else:
        st.write("No players registered yet.")

elif page == "Point Table":
    st.header("Point Table")

    # Display the point table for everyone
    st.dataframe(point_table.style.set_properties(**{'font-size': '16pt'}))

    # Admin section to edit the point table
    password = st.text_input("Enter Admin Password to Edit Point Table", type="password")

    if password == ADMIN_PASSWORD:
        st.write("### Edit Point Table")
        house = st.selectbox("Select House", point_table["House"].values)
        wins = st.number_input("Wins", min_value=0, step=1)
        losses = st.number_input("Losses", min_value=0, step=1)
        points = st.number_input("Points", min_value=0, step=1)

        if st.button("Update Points"):
            point_table.loc[point_table["House"] == house, "Wins"] = wins
            point_table.loc[point_table["House"] == house, "Losses"] = losses
            point_table.loc[point_table["House"] == house, "Points"] = points
            st.success(f"Updated points for {house}")

elif page == "Schedule":
    st.header("Match Schedule")

    # Display existing schedule for everyone
    if st.session_state.match_schedule:
        st.write("### Current Match Schedule")
        for match in st.session_state.match_schedule:
            st.write(f"- {match}")

    # Admin section to update match schedule
    password = st.text_input("Enter Admin Password to Fix Matches", type="password")

    if password == ADMIN_PASSWORD:
        st.write("### Add Match to Schedule")
        match_input = st.text_area("Enter Match Details")
        if st.button("Add Match"):
            if match_input:
                st.session_state.match_schedule.append(match_input)
                st.success("Match added to schedule!")
            else:
                st.error("Please enter match details.")

elif page == "Host Registration":
    st.header("Host Registration")

    # Display form but require admin password to register
    st.write("### Register as a Host")

    name = st.text_input("Name")
    contact_info = st.text_input("Contact Information")

    password = st.text_input("Enter Admin Password to Register as Host", type="password")

    if password == ADMIN_PASSWORD:
        if st.button("Register"):
            if name and contact_info:
                st.session_state.hosting_members.append({"Name": name, "Contact": contact_info})
                st.success(f"{name} has been registered as a host!")
            else:
                st.error("Please fill out all fields!")
    else:
        st.error("Incorrect admin password! You cannot register as a host.")

elif page == "Registration":
    st.image("Fft.png", width=500)  # Tournament logo
    st.write("### Welcome to the Free Fire Tournament!")

    # Form for registration
    form = st.form("registration_form")
    name = form.text_input("Name")
    class_selected = form.selectbox("Class", ["9", "10", "11", "12"])
    house = form.selectbox("House", ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])
    free_fire_uid = form.text_input("Free Fire UID")
    id_photo = form.file_uploader("Upload Your ID Photo", type=["jpg", "jpeg", "png"])

    submit = form.form_submit_button("Register")

    if submit:
        # Check if the player has already registered
        if free_fire_uid in registration_df["Free Fire UID"].values:
            st.error("You are already registered!")
        elif not name or not free_fire_uid or id_photo is None:
            st.error("All fields, including ID photo, are mandatory!")
        else:
            # Save the ID photo
            photo_path = os.path.join(ID_PHOTOS_DIR, f"{free_fire_uid}.jpg")
            with open(photo_path, "wb") as f:
                f.write(id_photo.getbuffer())
            st.session_state.player_photos[free_fire_uid] = photo_path  # Save the photo path

            # Append to the player DataFrame
            new_registration = {
                "Name": name,
                "Class": class_selected,
                "House": house,
                "Free Fire UID": free_fire_uid
            }
            registration_df = registration_df.append(new_registration, ignore_index=True)
            save_csv_data(registration_df, REGISTRATION_CSV)  # Save the updated data to CSV
            st.success(f"Registration successful for {name}!")

    # Always display the registration DataFrame
    if not registration_df.empty:
        st.write("### Registered Players")
        st.dataframe(registration_df)

elif page == "Notices":
    st.header("Notices")

    # Display existing notices for everyone
    if st.session_state.notices:
        st.write("### Existing Notices")
        for notice in st.session_state.notices:
            st.write(f"- {notice}")

    # Admin password input for adding notices
    password = st.text_input("Enter Admin Password to Add Notices", type="password")
    if password == ADMIN_PASSWORD:
        notice_input = st.text_area("Add a Notice")
        if st.button("Submit Notice"):
            if notice_input:
                st.session_state.notices.append(notice_input)
                st.success("Notice added!")
            else:
                st.error("Please enter a notice.")

elif page == "Rules":
    st.header("Rules")

    # Display existing rules for everyone
    if st.session_state.rules:
        st.write("### Existing Rules")
        for rule in st.session_state.rules:
            st.write(f"- {rule}")

    # Admin password input for adding rules
    password = st.text_input("Enter Admin Password to Add Rules", type="password")
    if password == ADMIN_PASSWORD:
        rule_input = st.text_area("Add a Rule")
        if st.button("Submit Rule"):
            if rule_input:
                st.session_state.rules.append(rule_input)
                st.success("Rule added!")
            else:
                st.error("Please enter a rule.")

elif page == "Connections":
    st.header("Connections")

    # Simple chat system (available for everyone)
    chat_message = st.text_input("Type your message")
    if st.button("Send"):
        if chat_message:
            st.session_state.chat_messages.append(chat_message)
            st.success("Message sent!")
        else:
            st.error("Message cannot be empty!")

    # Display chat messages
    if st.session_state.chat_messages:
        st.write("### Chat Messages")
        for message in st.session_state.chat_messages:
            st.write(message)

# Add a Twitter follow link at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("Follow me on [Twitter @SwapnilaSwayam](https://twitter.com/SwapnilaSwayam)")
