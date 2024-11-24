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
    menu_options = ["All Requisites", "Get Requisite", "Add Requisite", "Update Requisite", "Delete Requisite"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "classid" not in st.session_state:
        st.session_state.classid = ""

    if "reqid" not in st.session_state:
        st.session_state.reqid = ""

    if "set_button" not in st.session_state:
        st.session_state.set_button = False

    def clear():
        st.session_state.classid = ""
        st.session_state.reqid = ""
        st.session_state.set_button = False


    def allRequisites():
        st.header("All Requisites")
        try:
            response = requests.get(f"{BASE_URL}/requisite")
            if response.status_code == 200:
                requisites = response.json()

                df = pd.DataFrame(requisites)
                df.index = df.index + 1;
                st.dataframe(df, hide_index=True, height=500)
            else:
                st.error("Failed to fetch requisites.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def requisiteByIDs():
        st.header("Requisite by IDs")

        val1 = st.text_input("Class ID:")
        val2 = st.text_input("Req ID:")
        if st.button("Set IDs", type='primary'):
            st.session_state.set_button = True
            st.session_state.classid = val1
            st.session_state.reqid = val2

        if st.session_state.classid.isnumeric() and st.session_state.reqid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/requisite/{st.session_state.classid}/{st.session_state.reqid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500)
                    else:
                        st.warning("No data found for the Requisite IDs")
                else:
                    st.error(f"Failed to fetch Requisite: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Requisites":
        allRequisites()
    if st.session_state.option == "Get Requisite":
        clear()
        requisiteByIDs()
    # if selected_option == "Add Class":
    #     addClass()
    # if selected_option == "Update Class":
    #     updateClass()
    # if selected_option == "DeleteClass":
    #     deleteClass()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")