import streamlit as st
import pandas as pd

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Input Data", "View Analysis"])

    if page == "Input Data":
        data_collection_page()
    elif page == "View Analysis":
        data_analysis_page()

    # Move Twitter link to the bottom of the sidebar
    st.sidebar.title("Follow me on Twitter")
    twitter_handle = "SwapnilaSwayam"  # Replace with your actual Twitter handle
    twitter_url = f"https://twitter.com/{twitter_handle}"
    st.sidebar.markdown(f"[Follow @{twitter_handle} on Twitter]({twitter_url})")

def data_collection_page():
    st.title("Phone Usage and Its Impact on Studies")
    st.subheader("Data Collection for *Project Work*")

    # User inputs with validation checks
    name = st.text_input("Please enter your name:")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)
    gender = st.radio("Select your gender:", ["Male", "Female", "Other"])

    os = st.selectbox("Which OS do you use?", ["Android", "iOS"], help="Please select your phone's operating system.")

    usage_frequency = st.slider("Your average screen time (hours):", 0, 24, 1)

    # SelectBox for purpose with predefined options
    purpose_options = [
        "Studying", "Gaming", "Trading", "Social Media", "Watching Movies", 
        "Web Browsing", "Photography", "Content Creation", "Fitness Tracking",
        "Online Shopping", "Communication", "Other"
    ]
    purpose = st.selectbox("Select the primary purpose of your phone usage:", purpose_options)

    # SelectBox for activity with predefined options
    activity_options = [
        "Texting", "Calling", "Watching Videos", "Browsing Social Media", 
        "Playing Games", "Studying", "Trading", "Photography", "Content Creation", 
        "Shopping", "Other"
    ]
    activity = st.selectbox("Select the main activity you use your phone for:", activity_options)

    help_study = st.radio("Is your phone helpful for studying?", ["Yes", "No"])
    performance_impact = st.selectbox("Impact on your performance:", ["Improved", "Neutral", "Disimproved"])
    distraction = st.selectbox("Main source of distraction:", ["Short-form content", "Gaming", "Watching movies and web series", "Other"])
    usage_symptoms = st.selectbox("Symptoms you experience from phone usage:", ["None", "Headache", "Sleep disturbance", "Stress and anxiety"])
    symptom_frequency = st.selectbox("Frequency of symptoms:", ["Never", "Rarely", "Sometimes", "Frequently"])

    # Data to be saved
    data = {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "OS": os,
        "Usage Frequency": usage_frequency,
        "Purpose": purpose,
        "Activity": activity,
        "Helpful": help_study,
        "Performance Impact": performance_impact,
        "Distraction": distraction,
        "Usage Symptoms": usage_symptoms,
        "Symptom Frequency": symptom_frequency,
    }

    # Save button
    if st.button("Submit"):
        # Ensure all mandatory fields are filled
        if not name:
            st.error("Please enter your name.")
        elif not purpose:
            st.error("Please select the primary purpose of your phone usage.")
        elif not activity:
            st.error("Please select the main activity you use your phone for.")
        else:
            # Load existing data or create a new DataFrame
            try:
                df = pd.read_csv("phone_usage_data.csv")
                # Check if the CSV is empty
                if df.empty:
                    df = pd.DataFrame(columns=["Name", "Age", "Gender", "OS", "Usage Frequency", "Purpose", "Activity", "Helpful", "Performance Impact", "Distraction", "Usage Symptoms", "Symptom Frequency"])
            except FileNotFoundError:
                df = pd.DataFrame(columns=["Name", "Age", "Gender", "OS", "Usage Frequency", "Purpose", "Activity", "Helpful", "Performance Impact", "Distraction", "Usage Symptoms", "Symptom Frequency"])

            # Append new data to DataFrame
            new_data = pd.DataFrame([data])
            df = pd.concat([df, new_data], ignore_index=True)

            # Save DataFrame to CSV
            df.to_csv("phone_usage_data.csv", index=False)
            st.success("Data saved successfully!")

            # Display the DataFrame in the app
            st.dataframe(df)

            # Create a download button for the CSV file
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Press to Download",
                csv,
                "phone_usage_data.csv",
                "text/csv",
                key='download-csv'
            )

def data_analysis_page():
    st.title("Data Analysis")

    # Load data
    try:
        df = pd.read_csv("phone_usage_data.csv")

        if df.empty:
            st.warning("No data to analyze. Please submit some data first.")
        else:
            st.dataframe(df)
            
            # Descriptive statistics with a nice layout
            st.subheader("Descriptive Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Age", round(df["Age"].mean(), 2))
            with col2:
                st.metric("Minimum Age", df["Age"].min())
            with col3:
                st.metric("Maximum Age", df["Age"].max())

            st.metric("Average Screen Time (hours)", round(df["Usage Frequency"].mean(), 2))

            # Plotting graphs using Streamlit's built-in plotting functions
            st.subheader("Graphs")

            # Age Distribution
            st.write("Age Distribution")
            age_counts = df['Age'].value_counts().sort_index()
            st.bar_chart(age_counts)

            # Usage Frequency Distribution
            st.write("Usage Frequency Distribution")
            usage_counts = df['Usage Frequency'].value_counts().sort_index()
            st.bar_chart(usage_counts)

            # Performance Impact Distribution
            st.write("Performance Impact Distribution")
            performance_counts = df['Performance Impact'].value_counts()
            st.bar_chart(performance_counts)

            # Purpose Distribution
            st.write("Purpose Distribution")
            purpose_counts = df['Purpose'].value_counts()
            st.bar_chart(purpose_counts)

            # Activity Distribution
            st.write("Activity Distribution")
            activity_counts = df['Activity'].value_counts()
            st.bar_chart(activity_counts)

    except FileNotFoundError:
        st.error("No data available for analysis. Please submit some data first.")

if __name__ == "__main__":
    main()
