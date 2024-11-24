import streamlit as st
import pandas as pd
import requests

BASE_URL = "https://los-medallistas-c59825198b5f.herokuapp.com/los-medallistas/"

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
    menu_options = ["All Classes", "Get Class", "Add Class", "Update Class", "Delete Class"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "cid" not in st.session_state:
        st.session_state.cid = ""

    if "set_button" not in st.session_state:
        st.session_state.set_button = False

    def clear():
        st.session_state.cid = ""
        st.session_state.set_button = False


    def allClasses():
        st.header("All Rooms")
        try:
            response = requests.get(f"{BASE_URL}/class")
            if response.status_code == 200:
                classes = response.json()

                df = pd.DataFrame(classes)
                df.index = df.index + 1
                st.dataframe(df, hide_index=True, height=500)
                st.divider()
                st.divider()
                st.bar_chart(df['years'].value_counts(), x_label='Time Given', y_label='Number of Classes Given', color=(74, 69, 136), height=500)
            else:
                st.error("Failed to fetch classes.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def classByCID():
        st.header("Get Class by Class ID")

        val = st.text_input("Class ID:")

        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.cid = val

        if st.session_state.cid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/class/{st.session_state.cid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        st.dataframe(df)
                    else:
                        st.warning("No data found for the Room ID")
                else:
                    st.error(f"Failed to fetch Class: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Classes":
        allClasses()
    if st.session_state.option == "Get Class":
        clear()
        classByCID()
    # if selected_option == "Add Class":
    #     addClass()
    # if selected_option == "Update Class":
    #     updateClass()
    # if selected_option == "DeleteClass":
    #     deleteClass()
else:
    st.switch_page("../UI/login.py")
