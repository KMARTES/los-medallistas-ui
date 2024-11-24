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
    menu_options = ["All Meetings", "Get Meeting", "Add Meeting", "Update Meeting", "Delete Meeting"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "mid" not in st.session_state:
        st.session_state.mid = ""

    if "set_button" not in st.session_state:
        st.session_state.set_button = False


    def clear():
        st.session_state.mid = ""
        st.session_state.set_button = False


    def allMeetings():
        st.header("All Meetings")
        try:
            response = requests.get(f"{BASE_URL}/meeting")
            if response.status_code == 200:
                meetings = response.json()

                df = pd.DataFrame(meetings)
                st.dataframe(df, hide_index=True, height=500)
                st.divider()
                st.divider()
                st.bar_chart(df['cdays'].value_counts(), x_label='Days', y_label='Meetings', color=(187, 105, 105), height=500)
            else:
                st.error("Failed to fetch meetings.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def meetingByMID():
        st.header("Meeting by MID")
        val = st.text_input("Meeting ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.mid = val

        if st.session_state.mid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/meeting/{st.session_state.mid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        st.dataframe(df, hide_index=True, height=500)
                    else:
                        st.warning("No data found for the Room ID")
                else:
                    st.error(f"Failed to fetch Room: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Meetings":
        allMeetings()
    if st.session_state.option == "Get Meeting":
        clear()
        meetingByMID()
    # if selected_option == "Add Class":
    #     addClass()
    # if selected_option == "Update Class":
    #     updateClass()
    # if selected_option == "DeleteClass":
    #     deleteClass()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")