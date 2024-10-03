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
    pd.DataFrame(columns=["Name", "Class", "House", "Free Fire UID"]).to_csv(REGISTRATION_CSV, index=False)

# Load the registration data from the CSV file
def load_registration_data():
    return pd.read_csv(REGISTRATION_CSV)

# Save registration data to CSV
def save_registration_data(df):
    df.to_csv(REGISTRATION_CSV, index=False)

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
    "Connections"
])

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
            save_registration_data(registration_df)  # Save the updated data to CSV
            st.success(f"Registration successful for {name}!")

    # Always display the registration DataFrame
    if len(registration_df) > 0:
        st.write("### Registered Players")
        st.dataframe(registration_df)

elif page == "Host Registration":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Host Registration")
        new_member = st.text_input("Add a new hosting member")
        if st.button("Submit Member"):
            hosting_members.append(new_member)
        st.write("### Current Hosting Members")
        for member in hosting_members:
            st.write(member)
    else:
        st.error("You do not have permission to edit this page.")

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
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Schedule")
        available_teams = ["Aravali", "Nilgiri", "Shiwalik", "Udaygiri"]

        # Schedule matches, semifinals, and finals by the owner
        if len(available_teams) >= 2 and st.button("Schedule Match"):
            team1, team2 = random.sample(available_teams, 2)
            match_summary = f"Scheduled: {team1} vs {team2}"
            st.success(match_summary)

        st.write("### Last Match Details")
        if match_details:
            st.write(f"**Winner**: {match_details['Winner']}")
            st.write(f"**Rounds Won**: {match_details['Rounds Won by Team 1']} vs {match_details['Rounds Won by Team 2']}")
    else:
        st.error("You do not have permission to edit this page.")

elif page == "Point Table":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Point Table")
        st.dataframe(point_table)
    else:
        st.header("Point Table")
        st.dataframe(point_table)

elif page == "Player Stats":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Player Stats")
        # Example: Display highest kills per player
        # Add your stats here, e.g., by fetching from another DataFrame
    else:
        st.error("You do not have permission to edit this page.")

elif page == "Highlights":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Highlights")
        st.text_input("Add a highlight")  # For example, add highlights
    else:
        st.header("Highlights")
        st.write("View highlights from the event")

elif page == "Pictures":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Pictures")
        uploaded_photos = st.file_uploader("Upload photos from the event", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        if uploaded_photos:
            for uploaded_photo in uploaded_photos:
                photo_path = os.path.join(UPLOAD_DIR, uploaded_photo.name)
                with open(photo_path, "wb") as f:
                    f.write(uploaded_photo.getbuffer())
                st.image(photo_path, caption=uploaded_photo.name)
    else:
        st.error("You do not have permission to edit this page.")

elif page == "Payment":
    st.header("Payment")
    st.image("payment_qrcode.png", caption="Scan to Pay", width=200)
    st.write("UPI ID: your-upi-id@bank")

elif page == "Connections":
    password = st.text_input("Enter Admin Password", type="password")
    if password == ADMIN_PASSWORD:  # Owner access
        st.header("Connections")
        chat_message = st.text_input("Enter your message")
        if st.button("Send"):
            st.write(f"You: {chat_message}")
            # Here you can implement storing and displaying all user messages
    else:
        st
