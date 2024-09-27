import streamlit as st
import pandas as pd
import random
from PIL import Image

# Create a dictionary to store registration data
registrations = {}

# Create a dictionary to store team registrations
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}

# Create a dictionary to store hosting members' registrations
hosting_members = {}

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

# Create a point table board
point_table = pd.DataFrame({
    "House": ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"],
    "Wins": [0, 0, 0, 0],
    "Losses": [0, 0, 0, 0],
    "Points": [0, 0, 0, 0]
})

# Function to update points after each match
def update_points(winner, loser):
    global point_table
    point_table.loc[point_table["House"] == winner, "Wins"] += 1
    point_table.loc[point_table["House"] == loser, "Losses"] += 1
    point_table.loc[point_table["House"] == winner, "Points"] += 3  # Assuming 3 points for a win

# Function to get teams qualified for semifinals
def get_qualified_teams():
    sorted_table = point_table.sort_values(by="Points", ascending=False)
    return sorted_table["House"].iloc[:4].values  # Top 4 teams qualify for semifinals

# Function to determine the semifinal matchups (2 vs 3 and 1 vs 4)
def get_semifinal_matchups(qualified_teams):
    semifinal_1 = (qualified_teams[1], qualified_teams[2])  # 2 vs 3
    semifinal_2 = (qualified_teams[0], qualified_teams[3])  # 1 vs 4
    return semifinal_1, semifinal_2

# Function to determine the final match
def get_final_match(winner_semifinal_1, winner_semifinal_2):
    return (winner_semifinal_1, winner_semifinal_2)

# Create a Streamlit app
st.title("Free Fire League Registration")

# Add a sidebar to navigate between pages
page = st.sidebar.selectbox("Select a page", ["Registration", "Team Registration", "Match Fixing", "Semifinals", "Final", "Highlights", "Point Table", "Hosting Members"])

if page == "Registration":
    # Add a unique tournament logo at the top of the registration page
    st.image("Fft.png", width=500)  # Tournament logo
    st.write("### Welcome to the Free Fire Tournament!")

    # Registration form with limited class selection (9 to 12)
    form = st.form("registration_form")
    name = form.text_input("Name")
    class_selected = form.selectbox("Class", ["9", "10", "11", "12"])
    house = form.selectbox("House", ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])
    free_fire_uid = form.text_input("Free Fire UID")
    submit = form.form_submit_button("Register")

    # Store registration data
    if submit:
        registrations[name] = {"Class": class_selected, "House": house, "Free Fire UID": free_fire_uid}
        st.success(f"Registration successful for {name}!")

elif page == "Team Registration":
    # Register teams
    for name, details in registrations.items():
        house = details["House"]
        if len(team_registrations[house]) < 6:
            if name not in team_registrations[house]:  # Prevent duplicate registration
                team_registrations[house].append(name)

    # Display team registrations with logos and colors
    st.header("Team Registrations")
    for house, members in team_registrations.items():
        st.write(f"### {house} ({len(members)})")
        st.image(house_logos[house], width=50)
        st.write(f"Members: {', '.join(members)}")
        st.markdown(f"<div style='color:{house_colors[house]};'>------------------------</div>", unsafe_allow_html=True)

elif page == "Match Fixing":
    # Fix matches randomly
    matches = []
    for i in range(6):  # 6 matches per round
        match = []
        for house in team_registrations:
            if team_registrations[house]:
                match.append(random.choice(team_registrations[house]))
        matches.append(match)

    # Display matches and update points
    st.header("Match Fixing")
    for i, match in enumerate(matches):
        st.write(f"Match {i + 1}: {', '.join(match)}")
        if st.button(f"Set Winner for Match {i + 1}"):
            winner = random.choice(match)  # Random winner selection for now
            loser = [team for team in match if team != winner][0]  # Other team is the loser
            update_points(winner, loser)
            st.success(f"Winner: {winner}")

elif page == "Semifinals":
    # Get teams qualified for semifinals
    qualified_teams = get_qualified_teams()
    semifinal_1, semifinal_2 = get_semifinal_matchups(qualified_teams)

    st.header("Semifinals")
    st.write(f"Semifinal 1: {semifinal_1[0]} vs {semifinal_1[1]}")
    st.write(f"Semifinal 2: {semifinal_2[0]} vs {semifinal_2[1]}")

    # Set winners for semifinals
    if st.button("Set Winner for Semifinal 1"):
        winner_semifinal_1 = random.choice(semifinal_1)
        st.success(f"Winner of Semifinal 1: {winner_semifinal_1}")

    if st.button("Set Winner for Semifinal 2"):
        winner_semifinal_2 = random.choice(semifinal_2)
        st.success(f"Winner of Semifinal 2: {winner_semifinal_2}")

elif page == "Final":
    # Get final match details (based on semifinal winners)
    st.header("Final Match")
    st.write("The Final Match will be between the winners of the semifinals!")

    # Assume we already set semifinal winners
    final_match = get_final_match("Winner_Semifinal_1", "Winner_Semifinal_2")
    st.write(f"Final Match: {final_match[0]} vs {final_match[1]}")

    if st.button("Set Winner for Final"):
        winner_final = random.choice(final_match)
        st.success(f"The Champion of the Tournament is {winner_final}!")

elif page == "Highlights":
    # Display highlights
    st.header("Match Highlights")
    st.write("Watch the best moments from the matches below!")

    # Placeholder for match highlights URLs
    highlight_videos = {
        "Match 1": "https://example.com/match1_highlights",
        "Match 2": "https://example.com/match2_highlights",
        "Match 3": "https://example.com/match3_highlights",
    }

    for match, video_url in highlight_videos.items():
        st.subheader(match)
        st.video(video_url)

elif page == "Point Table":
    # Display point table
    st.header("Point Table")
    st.write(point_table)

elif page == "Hosting Members":
    # Registration form for hosting members
    form = st.form("hosting_member_form")
    name = form.text_input("Name")
    uid = form.text_input("UID")
    submit = form.form_submit_button("Register")

    # Store hosting members' registrations
    if submit:
        hosting_members[name] = {"UID": uid}
        st.success(f"Hosting member {name} registered successfully!")
