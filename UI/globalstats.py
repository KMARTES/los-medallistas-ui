import streamlit as st
import pandas as pd
import requests

BASE_URL = "https://streamlit-for-medallistas-e611ec6e2503.herokuapp.com/los-medallistas/"

login_page = st.Page("../UI/login.py", title="Log In", icon=":material/login:")
logout_page = st.Page("../UI/logout.py", title="Log Out", icon=":material/logout:")
classes = st.Page("../UI/classes.py", title="Classes", icon="📚")
rooms = st.Page("../UI/rooms.py", title="Rooms", icon="🏫")
requisite = st.Page("../UI/requisites.py", title="Requisite", icon="✅")
meetings = st.Page("../UI/meetings.py", title="Meetings", icon="📆")
sections = st.Page("../UI/sections.py", title="Sections", icon="▶️")
localstats = st.Page("../UI/localstats.py", title="LocalStats", icon="🇵🇷")
globalstats = st.Page("../UI/globalstats.py", title="GlobalStats", icon="🌎")
chatbot = st.Page("../UI/chatbot.py", title="Chatbot", icon="🤖")

st.set_page_config(layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Reports": [classes, requisite, rooms, meetings, sections],
            "Statistics": [localstats, globalstats],
            "Tools": [chatbot],
            "Account": [logout_page],
        }
    )

    # Create a horizontal menu using st.columns
    menu_options = ["Most Meetings", "Most Prerequisite", "Least Offered", "Total Sections"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.selected_option = option

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Most Meetings"

    def mostMeetings():
        st.header("Top 5 Meetings with the Most Sections.")

        try:
            response = requests.post(f"{BASE_URL}most/meeting")
            if response.status_code == 200:
                result = response.json()

                if result:
                    df = pd.DataFrame(result)
                    df.set_index(df['ccode'], inplace=True)
                    st.dataframe(df, hide_index=True)
                    st.divider()
                    st.divider()
                    st.bar_chart(df['sections'], x_label='Amount of Sections', y_label='Code', color=(190,197,105), horizontal=True, height=300)
                else:
                    st.error("Stat is unavailable.")
            else:
                st.error("Failed to fetch requested data.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")


    def mostPrerequisite():
        st.header("Top 3 Classes That Appears the Most as Prerequisite to Other Classes.")

        try:
            response = requests.post(f"{BASE_URL}most/prerequisite")
            if response.status_code == 200:
                result = response.json()

                if result:
                    df = pd.DataFrame(result)
                    df.set_index(df['ccode'], inplace=True)
                    st.dataframe(df, hide_index=True, column_order=['cname', 'ccode', 'appearances'])
                    st.divider()
                    st.divider()
                    st.bar_chart(df['appearances'], x_label='Appearances', y_label='Course Code', color=(190,197,105), horizontal=True, height=500)
                else:
                    st.error("Stat is unavailable.")
            else:
                st.error("Failed to fetch requested data.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def leastClasses():
        st.header("Top 3 Classes that were Offered the Least.")

        try:
            response = requests.post(f"{BASE_URL}least/classes")
            if response.status_code == 200:
                result = response.json()

                if result:
                    df = pd.DataFrame(result)
                    df.set_index(df['ccode'], inplace=True)
                    st.dataframe(df, hide_index=True, column_order=['cname', 'ccode', 'total_sections'])
                    st.divider()
                    st.divider()
                    st.bar_chart(df['total_sections'], x_label='Total Sections', y_label='Course Code', color=(190,197,105), horizontal=True, height=500)
            else:
                st.error("Failed to fetch requested data.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def totalSections():
        st.header("Total Number of Sections per Year")

        try:
            response = requests.post(f"{BASE_URL}section/year")
            if response.status_code == 200:
                result = response.json()

                if result:
                    df = pd.DataFrame(result)
                    df.set_index(df['years'], inplace=True)
                    st.dataframe(df, hide_index=True, column_order=['years', 'total_sections'])
                    st.divider()
                    st.divider()
                    st.bar_chart(df['total_sections'], x_label='Total Sections', y_label='Years', color=(190,197,105), horizontal=True, height=500)
            else:
                st.error("Failed to fetch requested data.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    if st.session_state.selected_option == "Most Meetings":
        mostMeetings()
    if st.session_state.selected_option == "Most Prerequisite":
        mostPrerequisite()
    if st.session_state.selected_option == "Least Offered":
        leastClasses()
    if st.session_state.selected_option == "Total Sections":
        totalSections()
else:
    st.switch_page("../UI/login.py")
