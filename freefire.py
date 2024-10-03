import streamlit as st
import pandas as pd
import random
import os

# Store registration and match data
registrations = []
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}
hosting_members = []
notices = []  # List to store notices
player_photos = {}  # Dictionary to store player ID photos
chat_messages = []  # Chat messages for Connections
match_details = []  # List to store match details

# Define house logos and colors
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
MATCH_SCHEDULE_CSV = "match_schedule.csv"  # CSV for match schedule
WINS_CSV = "wins.csv"  # CSV for storing wins
NOTICES_CSV = "notices.csv"  # CSV for storing notices
RULES_CSV = "rules.csv"  # CSV for storing rules

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
    "Rules",
    "Match Schedule",
    "Wins"
])

# Load the registration DataFrame from CSV
registration_df = load_csv_data(REGISTRATION_CSV)

if page == "Registration":
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
        elif not name or not free_fire_uid or not id_photo:
            st.error("All fields, including ID photo, are mandatory!")
        else:
            # Save the ID photo
            photo_path = os.path.join(ID_PHOTOS_DIR, f"{free_fire_uid}.jpg")
            with open(photo_path, "wb") as f:
                f.write(id_photo.getbuffer())
            player_photos[free_fire_uid] = photo_path

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
    if len(registration_df) > 0:
        st.write("### Registered Players")
        st.dataframe(registration_df)

elif page == "Host Registration":
    st.header("Host Registration")
    new_member = st.text_input("Add a new hosting member")
    if st.button("Submit Member"):
        hosting_members.append(new_member)
    st.write("### Current Hosting Members")
    for member in hosting_members:
        st.write(member)

elif page == "Team Info":
    st.header("Team Info")
    for house, members in team_registrations.items():
        st.write(f"### {house} ({len(members)})")
        st.image(house_logos[house], width=200)  # House logo

        # Display player information and ID photos of players
        house_members = registration_df[registration_df["House"] == house]
        if not house_members.empty:
            for player in house_members.to_dict(orient="records"):
                st.write(f"**Name**: {player['Name']}, **Class**: {player['Class']}, **Free Fire UID**: {player['Free Fire UID']}")

                if player["Free Fire UID"] in player_photos:
                    st.image(player_photos[player["Free Fire UID"]], caption=f"{player['Name']}'s ID", width=100)

elif page == "Schedule":
    st.header("Match Schedule")
    
    # Owner password input
    password = st.text_input("Enter Admin Password to Schedule Matches", type="password")
    
    if password == ADMIN_PASSWORD:
        # Owner can set matches
        teams = list(team_registrations.keys())
        
        # Match selection
        team1 = st.selectbox("Select Team 1", teams)
        team2 = st.selectbox("Select Team 2", teams)

        if team1 != team2:
            if st.button("Schedule Match"):
                rounds_won_team1 = random.randint(0, 5)
                rounds_won_team2 = 5 - rounds_won_team1
                winner = team1 if rounds_won_team1 > rounds_won_team2 else team2
                loser = team2 if winner == team1 else team1

                # Update points based on rounds
                point_table.loc[point_table["House"] == winner, "Wins"] += 1
                point_table.loc[point_table["House"] == loser, "Losses"] += 1
                point_table.loc[point_table["House"] == winner, "Points"] += rounds_won_team1 * 2
                point_table.loc[point_table["House"] == loser, "Points"] += rounds_won_team2 * 2

                match_summary = {
                    "Winner": winner,
                    "Loser": loser,
                    "Rounds Won by Team 1": rounds_won_team1,
                    "Rounds Won by Team 2": rounds_won_team2,
                }
                match_details.append(match_summary)

                # Save match details to CSV
                match_df = pd.DataFrame(match_details)
                save_csv_data(match_df, MATCH_SCHEDULE_CSV)

                st.success(f"Match Scheduled! Winner: {winner} | Rounds: {rounds_won_team1} - {rounds_won_team2}")
        
        # Display match results
        if match_details:
            st.write("### Match Results")
            for idx, match in enumerate(match_details):
                st.write(f"Match {idx + 1}: {match['Winner']} won against {match['Loser']} with rounds {match['Rounds Won by Team 1']} - {match['Rounds Won by Team 2']}")

    else:
        st.error("Incorrect Password! You do not have permission to schedule matches.")

elif page == "Point Table":
    st.header("Point Table")
    st.dataframe(point_table)

elif page == "Player Stats":
    st.header("Player Stats")
    # Example: Display highest kills per player
    st.write("Highest Kills per Player: (Functionality to be implemented)")

elif page == "Highlights":
    st.header("Highlights")
    st.write("View highlights from the event")

elif page == "Pictures":
    st.header("Pictures")
    uploaded_photos = st.file_uploader("Upload photos from the event", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    if uploaded_photos:
        for uploaded_photo in uploaded_photos:
            photo_path = os.path.join(UPLOAD_DIR, uploaded_photo.name)
            with open(photo_path, "wb") as f:
                f.write(uploaded_photo.getbuffer())
            st.image(photo_path, caption=uploaded_photo.name, width=200)

elif page == "Payment":
    st.header("Payment")
    st.write("Payment details and options")

elif page == "Connections":
    st.header("Connections")
    # Simple chat system
    chat_message = st.text_input("Type your message")
    if st.button("Send"):
        chat_messages.append(chat_message)
        st.experimental_rerun()  # Reload the page to show the new message

    # Display chat messages
    if chat_messages:
        st.write("### Chat Messages")
        for message in chat_messages:
            st.write(message)

elif page == "Notices":
    st.header("Notices")
    notices_df = load_csv_data(NOTICES_CSV)
    if not notices_df.empty:
        st.write(notices_df)

    notice_input = st.text_area("Add a Notice")
    if st.button("Submit Notice"):
        if notice_input:
            notices.append(notice_input)
            notices_df = notices_df.append({"Notice": notice_input}, ignore_index=True)
            save_csv_data(notices_df, NOTICES_CSV)  # Save the updated notices to CSV
            st.success("Notice added!")
        else:
            st.error("Please enter a notice.")

elif page == "Rules":
    st.header("Rules")
    rules_df = load_csv_data(RULES_CSV)
    if not rules_df.empty:
        st.write(rules_df)
    
    rule_input = st.text_area("Add a Rule")
    if st.button("Submit Rule"):
        if rule_input:
            rules_df = rules_df.append({"Rule": rule_input}, ignore_index=True)
            save_csv_data(rules_df, RULES_CSV)  # Save the updated rules to CSV
            st.success("Rule added!")
        else:
            st.error("Please enter a rule.")

elif page == "Match Schedule":
    st.header("Match Schedule")
    match_schedule_df = load_csv_data(MATCH_SCHEDULE_CSV)
    if not match_schedule_df.empty:
        st.write("### Scheduled Matches")
        st.dataframe(match_schedule_df)
    else:
        st.write("No matches scheduled yet.")

elif page == "Wins":
    st.header("Wins")
    wins_df = load_csv_data(WINS_CSV)
    if not wins_df.empty:
        st.write("### Win Records")
        st.dataframe(wins_df)
    else:
        st.write("No wins recorded yet.")

# Add Twitter follow link at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("Follow me on [Twitter @SwapnilaSwayam](https://twitter.com/SwapnilaSwayam)")
