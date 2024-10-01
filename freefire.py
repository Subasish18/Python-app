
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
last_played_team = None  # Track last played team to avoid consecutive matches
match_details = None  # Store the details of the last match played

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
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ID_PHOTOS_DIR, exist_ok=True)

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

# Function to simulate the match
def play_match(team1, team2):
    rounds_won_team1 = random.randint(0, 5)
    rounds_won_team2 = 5 - rounds_won_team1
    winner = team1 if rounds_won_team1 > rounds_won_team2 else team2
    loser = team2 if winner == team1 else team1
    update_points(winner, loser, max(rounds_won_team1, rounds_won_team2))
    
    # Store match details
    match_summary = {
        "Winner": winner,
        "Loser": loser,
        "Rounds Won by Team 1": rounds_won_team1,
        "Rounds Won by Team 2": rounds_won_team2,
    }
    return match_summary

# Function to check if a player is already registered by their Free Fire UID
def is_player_registered(uid, registration_df):
    return uid in registration_df["Free Fire UID"].values

# Streamlit app starts here
st.title("Free Fire League Registration")

# Add a sidebar to navigate between pages
page = st.sidebar.selectbox("Select a page", ["Registration", "Team Registration", "Match Fixing", "Semifinals", "Final", "Highlights", "Point Table", "Notices", "Hosting Members", "Photo Upload"])

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
    st.header("Team Registrations")
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

elif page == "Match Fixing":
    st.header("Match Fixing")

    available_teams = ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"]

    # Randomly select two different teams for the match
    if len(available_teams) < 2:
        st.error("Not enough teams to play a match.")
    else:
        team1, team2 = random.sample(available_teams, 2)

        if st.button("Play Match"):
            global match_details  # Use global to keep match details accessible
            match_details = play_match(team1, team2)
            st.success(f"{match_details['Winner']} won the match!")
            st.write(f"**Match Summary**: {team1} won {match_details['Rounds Won by Team 1']} rounds, {team2} won {match_details['Rounds Won by Team 2']} rounds.")
            
            # Display updated points table
            st.header("Updated Point Table")
            st.dataframe(point_table)

    # Display last match details if available
    if match_details:
        st.write("### Last Match Details")
        st.write(f"**Winner**: {match_details['Winner']}")
        st.write(f"**Rounds Won by {team1}**: {match_details['Rounds Won by Team 1']}")
        st.write(f"**Rounds Won by {team2}**: {match_details['Rounds Won by Team 2']}")

elif page == "Point Table":
    st.header("Point Table")
    st.dataframe(point_table)

elif page == "Semifinals":
    semifinal_teams = point_table.nlargest(2, 'Points')['House'].values
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
