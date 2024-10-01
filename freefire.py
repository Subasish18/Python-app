import streamlit as st
import pandas as pd
import random
from PIL import Image
import os

# Store registration and match data
registrations = []
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}
hosting_members = []
notices = []  # List to store notices
player_photos = {}  # Dictionary to store player ID photos
last_played_team = None  # Track last played team to avoid consecutive matches

# Define house logos and colors
house_logos = {
    "Aravali": "Arv.png",  
    "Nilgiri": "Nil.png",  
    "Shiwalik": "Shiw.jpeg",  
    "Udaygiri": "Udi.jpeg"  
}
house_colors = {
    "Aravali": "#0000FF",  
    "Nilgiri": "#008000",  
    "Shiwalik": "#FF0000",  
    "Udaygiri": "#FFFF00"  
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
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
if not os.path.exists(ID_PHOTOS_DIR):
    os.makedirs(ID_PHOTOS_DIR)

# Ensure the CSV file exists
if not os.path.exists(REGISTRATION_CSV):
    # Create an empty CSV file if it doesn't exist
    pd.DataFrame(columns=["Name", "Class", "House", "Free Fire UID"]).to_csv(REGISTRATION_CSV, index=False)

# Load the registration data from the CSV file
def load_registration_data():
    return pd.read_csv(REGISTRATION_CSV)

# Save registration data to CSV
def save_registration_data(df):
    df.to_csv(REGISTRATION_CSV, index=False)

# Function to update points based on rounds
def update_points(winner, loser, rounds_won_by_winner):
    points_for_winner = rounds_won_by_winner * 2
    points_for_loser = (5 - rounds_won_by_winner) * 2

    point_table.loc[point_table["House"] == winner, "Wins"] += 1
    point_table.loc[point_table["House"] == loser, "Losses"] += 1
    point_table.loc[point_table["House"] == winner, "Points"] += points_for_winner
    point_table.loc[point_table["House"] == loser, "Points"] += points_for_loser

# Function to get the top 2 teams for semifinals
def get_semifinal_teams():
    sorted_table = point_table.sort_values(by="Points", ascending=False)
    return sorted_table["House"].iloc[:2].values  # Top 2 teams qualify for semifinals

# Function to simulate the match
def play_match(team1, team2):
    rounds_won_team1 = random.randint(0, 5)
    rounds_won_team2 = 5 - rounds_won_team1
    winner = team1 if rounds_won_team1 > rounds_won_team2 else team2
    loser = team2 if winner == team1 else team1
    update_points(winner, loser, max(rounds_won_team1, rounds_won_team2))
    return winner, loser, rounds_won_team1, rounds_won_team2

# Function to check if a player is already registered by their Free Fire UID
def is_player_registered(uid, registration_df):
    return uid in registration_df["Free Fire UID"].values

# Function to restrict public from editing and give owner access
def owner_access(owner_password):
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password == owner_password:
        st.sidebar.success("Access granted as owner.")
        return True
    else:
        st.sidebar.warning("Incorrect password. View-only mode enabled.")
        return False

# Streamlit app starts here
st.title("Free Fire League Registration")

# Add a sidebar to navigate between pages
page = st.sidebar.selectbox("Select a page", ["Registration", "Team Registration", "Match Fixing", "Semifinals", "Final", "Highlights", "Point Table", "Notices", "Hosting Members", "Photo Upload"])

# Owner password for managing access (set your password here)
OWNER_PASSWORD = "linkan737"

# Load the registration DataFrame from CSV
registration_df = load_registration_data()

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
        if is_player_registered(free_fire_uid, registration_df):
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
            save_registration_data(registration_df)  # Save the updated data to CSV
            st.success(f"Registration successful for {name}!")

    # Display the registration DataFrame
    if len(registration_df) > 0:
        st.write("### Registered Players")
        st.dataframe(registration_df)

elif page == "Team Registration":
    # Team registration is open for players
    st.header("Team Registrations")
    for house, members in team_registrations.items():
        st.write(f"### {house} ({len(members)})")
        st.image(house_logos[house], width=200)  # House logo
        
        st.write(f"Members: {', '.join(members)}")
        st.markdown(f"<div style='color:{house_colors[house]};'>------------------------</div>", unsafe_allow_html=True)
        
        # Display player information and ID photos of players
        for player in registration_df.to_dict(orient="records"):
            if player["House"] == house:
                st.write(f"**Name**: {player['Name']}, **Class**: {player['Class']}, **Free Fire UID**: {player['Free Fire UID']}")
                
                if player["Free Fire UID"] in player_photos:
                    st.image(player_photos[player["Free Fire UID"]], caption=f"{player['Name']}'s ID", width=100)

elif page == "Match Fixing":
    st.header("Match Fixing")

    # Prevent consecutive matches for the same team
    global last_played_team
    
    available_teams = ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"]
    if last_played_team:
        available_teams.remove(last_played_team)  # Remove last played team from available options

    # Dropdown to select teams for the match
    team1 = st.selectbox("Select Team 1", available_teams)
    team2 = st.selectbox("Select Team 2", [house for house in available_teams if house != team1])

    if st.button("Play Match"):
        winner, loser, rounds_won_team1, rounds_won_team2 = play_match(team1, team2)
        last_played_team = winner  # Update last played team
        st.success(f"{winner} won the match!")
        st.write(f"**Match Summary**: {team1} won {rounds_won_team1} rounds, {team2} won {rounds_won_team2} rounds.")
        
        # Display updated points table
        st.header("Updated Point Table")
        st.dataframe(point_table)

elif page == "Point Table":
    st.header("Point Table")
    st.dataframe(point_table)

elif page == "Semifinals":
    semifinal_teams = get_semifinal_teams()
    st.header("Semifinal Teams")
    st.write(f"The top 2 teams qualifying for the semifinals are: {', '.join(semifinal_teams)}")

elif page == "Notices":
    st.header("Notices")
    new_notice = st.text_input("Add a new notice")
    if st.button("Submit Notice"):
        notices.append(new_notice)
    st.write("### Current Notices")
    for notice in notices:
        st.write(notice)

elif page == "Hosting Members":
    st.header("Hosting Members")
    new_member = st.text_input("Add a new hosting member")
    if st.button("Submit Member"):
        hosting_members.append(new_member)
    st.write("### Current Hosting Members")
    for member in hosting_members:
        st.write(member)

elif page == "Photo Upload":
    st.header("Upload Event Photos")
    uploaded_photos = st.file_uploader("Upload photos from the event", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    if uploaded_photos:
        for uploaded_photo in uploaded_photos:
            photo_path = os.path.join(UPLOAD_DIR, uploaded_photo.name)
            with open(photo_path, "wb") as f:
                f.write(uploaded_photo.getbuffer())
            st.image(photo_path, caption=uploaded_photo.name)

# Add Twitter follow link at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("Follow me on [Twitter @SwapnilaSwayam](https://twitter.com/SwapnilaSwayam)")
