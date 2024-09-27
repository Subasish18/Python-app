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
    "Aravali": " Arv.png",  # Blue rifle logo
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

# Create a Streamlit app
st.title("Free Fire League Registration")

# Add a sidebar to navigate between pages
page = st.sidebar.selectbox("Select a page", ["Registration", "Team Registration", "Match Fixing", "Highlights", "Point Table", "Hosting Members", "Final Match"])

if page == "Registration":
    # Add a unique tournament logo at the top of the registration page
    st.image("Fft.png", width=500)  # Tournament logo (replace with your preferred URL)
    st.write("### Welcome to the Free Fire Tournament!")

    # Registration form with limited class selection (9 to 12)
    form = st.form("registration_form")
    name = form.text_input("Name")
    class_selected = form.selectbox("Class", ["9", "10", "11", "12"])  # Renamed class_level to class_selected
    house = form.selectbox("House", ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"])
    free_fire_uid = form.text_input("Free Fire UID")
    submit = form.form_submit_button("Register")

    # Store registration data
    if submit:
        registrations[name] = {"Class": class_selected, "House": house, "Free Fire UID": free_fire_uid}
        st.success("Registration successful!")

elif page == "Team Registration":
    # Register teams
    for name, details in registrations.items():
        house = details["House"]
        if len(team_registrations[house]) < 6:
            if name not in team_registrations[house]:  # Prevent duplicate registration
                team_registrations[house].append(name)
        else:
            st.error("Team registration full for {}".format(house))

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

    # Display matches
    st.header("Match Fixing")
    for i, match in enumerate(matches):
        st.write(f"Match {i+1}: {', '.join(match)}")

elif page == "Highlights":
    # Display highlights instead of live stream
    st.header("Match Highlights")
    st.write("Watch the best moments from the matches below!")

    # Placeholder for match highlights URLs (replace with actual video URLs)
    highlight_videos = {
        "Match 1": "https://example.com/match1_highlights",
        "Match 2": "https://example.com/match2_highlights",
        "Match 3": "https://example.com/match3_highlights",
    }

    for match, video_url in highlight_videos.items():
        st.subheader(match)
        st.video(video_url)  # Use video URL

elif page == "Point Table":
    # Create a point table board
    point_table = pd.DataFrame(columns=["House", "Wins", "Losses", "Points"])
    for house in team_registrations:
        point_table = pd.concat([point_table, pd.DataFrame({"House": [house], "Wins": [0], "Losses": [0], "Points": [0]})], ignore_index=True)

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

elif page == "Final Match":
    st.header("Final Match")
    st.write("Details will be available soon!")

# Add a "Follow me on Twitter" link at the bottom of the sidebar
st.sidebar.markdown("[Follow me on Twitter](https://twitter.com/SwapnilaSwayam)")
