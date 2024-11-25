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

    if "ccode" "starttime" "endtime" "cdays" not in st.session_state:
        st.session_state.ccode = ""
        st.session_state.starttime = ""
        st.session_state.endtime = ""
        st.session_state.cdays = ""

    def clear():
        st.session_state.mid = ""
        st.session_state.ccode = ""
        st.session_state.starttime = ""
        st.session_state.endtime = ""
        st.session_state.cdays = ""
        st.session_state.set_button = False


    def allMeetings():
        st.header("All Meetings")
        try:
            response = requests.get(f"{BASE_URL}meeting")
            if response.status_code == 200:
                meetings = response.json()

                df = pd.DataFrame(meetings)
                st.dataframe(df, hide_index=True, height=500, column_order=['mid', 'ccode', 'starttime', 'endtime', 'cdays'])
                st.divider()
                st.divider()
                st.bar_chart(df['cdays'].value_counts(), x_label='Days', y_label='Meetings', color=(187, 105, 105), height=500)
            else:
                st.error(f"Failed to fetch meetings: {response.status_code} - {response.text}")
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
                response = requests.get(f"{BASE_URL}meeting/{st.session_state.mid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        st.dataframe(df, hide_index=True, column_order=['mid', 'ccode', 'starttime', 'endtime', 'cdays'])
                    else:
                        st.warning("No data found for the Meeting ID")
                else:
                    st.error(f"Failed to fetch meeting: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def addMeeting():
        st.header("Add Meeting")

        ccode = st.text_input("Meeting Code:")
        starttime = st.text_input("Meeting Start Time: Format -> 00:00:00")
        endtime = st.text_input("Meeting End Time: Format -> 00:00:00")
        cdays = st.text_input("Meeting Days:")

        if st.button("Add", type='primary'):
            st.session_state.set_button = True
            st.session_state.ccode = ccode
            st.session_state.starttime = pd.to_datetime(starttime).strftime("%H:%M:%S")
            st.session_state.endtime = pd.to_datetime(endtime).strftime("%H:%M:%S")
            st.session_state.cdays = cdays

            data = {"ccode": ccode, "starttime": st.session_state.starttime, "endtime": st.session_state.endtime, "cdays": cdays}

        if st.session_state.ccode and st.session_state.starttime and st.session_state.endtime and st.session_state.cdays:
            try:
                response = requests.post(f"{BASE_URL}meeting", json=data)

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.dataframe([result])
                    else:
                        st.warning("No data added to Meeting table.")
                else:
                    st.error(f"Failed to add meeting: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def updateMeeting():
        st.header("Update Meeting")

        mid = st.text_input("Meeting ID:")
        ccode = st.text_input("Meeting Code:")
        starttime = st.text_input("Meeting Start Time: Format -> 00:00:00")
        endtime = st.text_input("Meeting End Time: Format -> 00:00:00")
        cdays = st.text_input("Meeting Days:")

        if st.button("Update", type='primary'):
            st.session_state.set_button = True
            st.session_state.mid = mid
            st.session_state.ccode = ccode
            st.session_state.starttime = pd.to_datetime(starttime).strftime("%H:%M:%S")
            st.session_state.endtime = pd.to_datetime(endtime).strftime("%H:%M:%S")
            st.session_state.cdays = cdays

            data = {"mid": mid, "ccode": ccode, "starttime": st.session_state.starttime, "endtime": st.session_state.endtime, "cdays": cdays}

        if st.session_state.mid and st.session_state.ccode and st.session_state.starttime and st.session_state.endtime and st.session_state.cdays:
            try:
                response = requests.put(f"{BASE_URL}meeting/{mid}", json=data)

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.dataframe([result])
                    else:
                        st.warning("No data added to Meeting table.")
                else:
                    st.error(f"Failed to update meeting; verify parameters: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def deleteMeeting():
        st.header("Delete Meeting by MID")

        val = st.text_input("Meeting ID:")

        if st.button("Delete", type='primary'):
            st.session_state.set_button = True
            st.session_state.mid = val

        if st.session_state.mid:
            try:
                response = requests.delete(f"{BASE_URL}meeting/{val}")

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.dataframe([result])
                    else:
                        st.warning("No meeting ID found.")
                else:
                    st.error(f"Failed to delete meeting: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Meetings":
        allMeetings()
    if st.session_state.option == "Get Meeting":
        clear()
        meetingByMID()
    if st.session_state.option == "Add Meeting":
        clear()
        addMeeting()
    if st.session_state.option == "Update Meeting":
        clear()
        updateMeeting()
    if st.session_state.option == "Delete Meeting":
        clear()
        deleteMeeting()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")