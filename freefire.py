import streamlit as st
import pandas as pd
import random
from PIL import Image

# Store registration and match data
registrations = []
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}
hosting_members = []
notices = []  # List to store notices

# Define house logos and colors
house_logos = {
    "Aravali": "Arv.png",  # Blue rifle logo
    "Nilgiri": "Nil.png",  # Green sniper logo
    "Shiwalik": "Shiw.jpeg",  # Red shotgun logo
    "Udaygiri": "Udi.jpeg"  # Yellow pistol logo
}
house_colors = {
    "Aravali": "#0000FF",  # Blue
    "Nilgiri": "#008000",  # Green
    "Shiwalik": "#FF0000",  # Red
    "Udaygiri": "#FFFF00"  # Yellow
}

# Points table for tracking scores
point_table = pd.DataFrame({
    "House": ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"],
    "Wins": [0, 0, 0, 0],
    "Losses": [0, 0, 0, 0],
    "Points": [0, 0, 0, 0]
})

# Function to update points based on rounds
def update_points(winner, loser, rounds_won_by_winner):
    global point_table
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
    submit = form.form_submit_button("Register")

    if submit:
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

elif page == "Hosting Members":
    if owner_access(OWNER_PASSWORD):
        st.header("Register Hosting Members")
        
        # Form for host member registration
        form = st.form("hosting_member_form")
        name = form.text_input("Name")
        uid = form.text_input("UID")
        submit = form.form_submit_button("Register")

        if submit:
            # Append to the hosting members DataFrame
            hosting_members.append({
                "Name": name,
                "UID": uid
            })
            host_member_df = pd.DataFrame(hosting_members)
            st.success(f"Hosting member {name} registered successfully!")
    
    # Display the host member DataFrame
    if len(hosting_members) > 0:
        st.write("### Registered Hosting Members")
        st.dataframe(host_member_df)

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

elif page == "Match Fixing":
    if owner_access(OWNER_PASSWORD):
        houses = list(team_registrations.keys())
        matches = [(houses[i], houses[j]) for i in range(len(houses)) for j in range(i+1, len(houses))]

        st.header("Match Fixing")
        for i, (team1, team2) in enumerate(matches):
            st.write(f"Match {i + 1}: {team1} vs {team2}")
            if st.button(f"Play Match {i + 1}"):
                winner, loser, rounds_won_winner, rounds_won_loser = play_match(team1, team2)
                st.success(f"Winner: {winner} ({rounds_won_winner} rounds won)")
                st.warning(f"Loser: {loser} ({rounds_won_loser} rounds won)")

elif page == "Photo Upload":
    st.header("Uploaded Photos")
    # Image uploading will only be available to the owner
    if owner_access(OWNER_PASSWORD):
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image.", use_column_width=True)
            st.success("Image uploaded successfully!")
    else:
        st.warning("Only the owner can upload images.")

# Add a "Follow me on Twitter" link at the bottom of the sidebar
st.sidebar.markdown("[Follow me on Twitter](https://twitter.com/SwapnilaSwayam)")
