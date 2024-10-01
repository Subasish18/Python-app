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

# Directory to store uploaded images
UPLOAD_DIR = "uploaded_photos"
ID_PHOTOS_DIR = "id_photos"

# Ensure the upload directories exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
if not os.path.exists(ID_PHOTOS_DIR):
    os.makedirs(ID_PHOTOS_DIR)

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
def is_player_registered(uid):
    for player in registrations:
        if player["Free Fire UID"] == uid:
            return True
    return False

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

# DataFrames for registered players and hosting members
player_df = pd.DataFrame(columns=["Name", "Class", "House", "Free Fire UID"])
host_member_df = pd.DataFrame(columns=["Name", "UID"])

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
        if is_player_registered(free_fire_uid):
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
            registrations.append({
                "Name": name,
                "Class": class_selected,
                "House": house,
                "Free Fire UID": free_fire_uid
            })
            player_df = pd.DataFrame(registrations)
            st.success(f"Registration successful for {name}!")

    # Display the registration DataFrame
    if len(registrations) > 0:
        st.write("### Registered Players")
        st.dataframe(player_df)

elif page == "Team Registration":
    # Team registration is open for players
    for player in registrations:
        house = player["House"]
        if len(team_registrations[house]) < 6 and player["Name"] not in team_registrations[house]:
            team_registrations[house].append(player["Name"])

    st.header("Team Registrations")
    for house, members in team_registrations.items():
        st.write(f"### {house} ({len(members)})")
        st.image(house_logos[house], width=200)  # Increased logo size to 200
        st.write(f"Members: {', '.join(members)}")
        st.markdown(f"<div style='color:{house_colors[house]};'>------------------------</div>", unsafe_allow_html=True)

        # Display ID photos of players
        st.write(f"**ID Photos for {house} Players:**")
        for player in registrations:
            if player["House"] == house and player["Free Fire UID"] in player_photos:
                st.image(player_photos[player["Free Fire UID"]], caption=f"{player['Name']}'s ID", width=100)

elif page == "Match Fixing":
    houses = list(team_registrations.keys())
    matches = [(houses[i], houses[j]) for i in range(len(houses)) for j in range(i+1, len(houses))]

    st.header("Match Fixing")
    for i, (team1, team2) in enumerate(matches):
        st.write(f"Match {i + 1}: {team1} vs {team2}")
        if st.button(f"Play Match {i + 1}"):
            winner, loser, rounds_won_winner, rounds_won_loser = play_match(team1, team2)
            st.success(f"Winner: {winner} ({rounds_won_winner} rounds won)")
            st.warning(f"Loser: {loser} ({rounds_won_loser} rounds won)")

elif page == "Notices":
    st.header("Notices")

    # Display notices to the public
    if len(notices) > 0:
        for notice in notices:
            st.write(f"- {notice}")
    else:
        st.write("No notices available.")
    
    # Only the owner can add or modify notices
    if owner_access(OWNER_PASSWORD):
        new_notice = st.text_input("Add a new notice")
        if st.button("Add Notice") and new_notice:
            notices.append(new_notice)
            st.success(f"Notice added: {new_notice}")

elif page == "Point Table":
    st.header("Point Table")
    st.dataframe(point_table)

elif page == "Semifinals":
    semifinal_teams = get_semifinal_teams()
    st.header("Semifinal Teams")
    st.write(f"The top 2 teams qualifying for the semifinals are: {', '.join(semifinal_teams)}")

elif page == "Final":
    semifinal_teams = get_semifinal_teams()
    st.header("Final Teams")
    if len(semifinal_teams) == 2:
        final_winner, final_loser, _, _ = play_match(semifinal_teams[0], semifinal_teams[1])
        st.write(f"The final winner is: {final_winner}")
        st.write(f"The runner-up is: {final_loser}")
    else:
        st.write("Not enough teams to play the final yet.")

elif page == "Photo Upload":
    st.header("Uploaded Photos")
    
    # Display previously uploaded images
    if os.listdir(UPLOAD_DIR):
        for image_file in os.listdir(UPLOAD_DIR):
            img = Image.open(os.path.join(UPLOAD_DIR, image_file))
            st.image(img, caption=f"Uploaded Photo: {image_file}", use_column_width=True)
    else:
        st.write("No photos uploaded yet.")
    
    # Only the owner can upload new photos
    if owner_access(OWNER_PASSWORD):
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            # Save the uploaded image to the UPLOAD_DIR
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Image {uploaded_file.name} uploaded successfully!")
