import streamlit as st
import pandas as pd
import random
from PIL import Image

# Store registration and match data
registrations = {}
team_registrations = {"Aravali": [], "Nilgiri": [], "Shiwalik": [], "Udaygiri": []}
hosting_members = {}
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
page = st.sidebar.selectbox("Select a page", ["Registration", "Team Registration", "Match Fixing", "Semifinals", "Final", "Highlights", "Point Table", "Notices", "Hosting Members"])

# Owner password for managing access (set your password here)
OWNER_PASSWORD = "linkan737"

if page == "Registration":
    st.image("Fft.png", width=500)  # Tournament logo
    st.write("### Welcome to the Free Fire Tournament!")
    form = st.form("registration_form")
    name = form.text_input("Name")
    class_selected = form.selectbox("Class", ["9", "10", "11", "12"])
    house = form.selectbox("House", ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])
    free_fire_uid = form.text_input("Free Fire UID")
    submit = form.form_submit_button("Register")

    if submit:
        registrations[name] = {"Class": class_selected, "House": house, "Free Fire UID": free_fire_uid}
        st.success(f"Registration successful for {name}!")

elif page == "Team Registration":
    # Team registration is open for players
    for name, details in registrations.items():
        house = details["House"]
        if len(team_registrations[house]) < 6 and name not in team_registrations[house]:
            team_registrations[house].append(name)

    st.header("Team Registrations")
    for house, members in team_registrations.items():
        st.write(f"### {house} ({len(members)})")
        st.image(house_logos[house], width=50)
        st.write(f"Members: {', '.join(members)}")
        st.markdown(f"<div style='color:{house_colors[house]};'>------------------------</div>", unsafe_allow_html=True)

elif page == "Match Fixing":
    if owner_access(OWNER_PASSWORD):
        matches = []
        for i in range(6):
            match = []
            for house in team_registrations:
                if team_registrations[house]:
                    match.append(random.choice(team_registrations[house]))
            matches.append(match)

        st.header("Match Fixing")
        for i, match in enumerate(matches):
            st.write(f"Match {i + 1}: {', '.join(match)}")
            winner = st.selectbox(f"Select Winner for Match {i + 1}", match)
            if st.button(f"Set Winner for Match {i + 1}"):
                loser = [team for team in match if team != winner][0]
                rounds_won_by_winner = random.randint(3, 5)  # Random number of rounds won by the winner
                update_points(winner, loser, rounds_won_by_winner)
                st.success(f"Winner: {winner} with {rounds_won_by_winner} rounds won!")
    else:
        st.header("View Match Fixing")
        st.write("Only the owner can update match fixing. Please contact the administrator for access.")

elif page == "Semifinals":
    if owner_access(OWNER_PASSWORD):
        semifinal_teams = get_semifinal_teams()
        st.header("Semifinal Match")
        team1 = st.selectbox("Select Semifinalist 1", semifinal_teams)
        team2 = st.selectbox("Select Semifinalist 2", [team for team in semifinal_teams if team != team1])

        if st.button("Set Semifinalist Teams"):
            st.success(f"Semifinal teams set: {team1} vs {team2}")

        if st.button("Play Semifinal"):
            winner, loser, rounds_won_winner, rounds_won_loser = play_match(team1, team2)
            st.success(f"Semifinal Winner: {winner} ({rounds_won_winner} rounds won)")
            st.warning(f"Semifinal Loser: {loser} ({rounds_won_loser} rounds won)")
    else:
        st.header("View Semifinals")
        st.write("Only the owner can set or play the semifinals. Please contact the administrator for access.")

elif page == "Final":
    if owner_access(OWNER_PASSWORD):
        semifinal_winner = st.selectbox("Select Finalist from Semifinal Winner", ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])  # Manual selection
        other_finalist = st.selectbox("Select the Other Finalist", ["TBD", "Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])

        if st.button("Set Finalist Teams"):
            st.success(f"Final match set: {semifinal_winner} vs {other_finalist}")

        if st.button("Play Final"):
            winner, loser, rounds_won_winner, rounds_won_loser = play_match(semifinal_winner, other_finalist)
            st.success(f"Final Winner: {winner} ({rounds_won_winner} rounds won)")
            st.warning(f"Final Loser: {loser} ({rounds_won_loser} rounds won)")
    else:
        st.header("View Final")
        st.write("Only the owner can set or play the final. Please contact the administrator for access.")

elif page == "Point Table":
    if owner_access(OWNER_PASSWORD):
        st.header("Edit Point Table")
        st.write(point_table)

        for index, row in point_table.iterrows():
            st.text(f"Edit points for {row['House']}:")
            wins = st.number_input(f"Wins for {row['House']}", value=row["Wins"], key=f"wins_{index}")
            losses = st.number_input(f"Losses for {row['House']}", value=row["Losses"], key=f"losses_{index}")
            points = st.number_input(f"Points for {row['House']}", value=row["Points"], key=f"points_{index}")

            if st.button(f"Update {row['House']}"):
                point_table.at[index, 'Wins'] = wins
                point_table.at[index, 'Losses'] = losses
                point_table.at[index, 'Points'] = points
                st.success(f"Updated points for {row['House']}")

    else:
        st.header("View Point Table")
        st.write(point_table)

elif page == "Notices":
    # Display notices for all users
    st.header("Notices")
    if owner_access(OWNER_PASSWORD):
        notice = st.text_area("Post a Notice", height=100)
        if st.button("Post Notice"):
            if notice:
                notices.append(notice)
                st.success("Notice posted successfully!")
            else:
                st.warning("Notice cannot be empty!")

    # Show all notices
    for i, notice in enumerate(notices):
        st.write(f"**Notice {i + 1}:** {notice}")

elif page == "Hosting Members":
    if owner_access(OWNER_PASSWORD):
        form = st.form("hosting_member_form")
        name = form.text_input("Name")
        uid = form.text_input("UID")
        submit = form.form_submit_button("Register")

        if submit:
            hosting_members[name] = {"UID": uid}
            st.success(f"Hosting member {name} registered successfully!")
    else:
        st.warning("Only hosting members can register here.")
