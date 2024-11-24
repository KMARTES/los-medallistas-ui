import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

BASE_URL = "https://los-medallistas-c59825198b5f.herokuapp.com/los-medallistas"

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
    menu_options = ["All Sections", "Get Section", "Add Section", "Update Section", "Delete Section"]
    selected_option = None
    widths = [len(option) for option in menu_options]

    with st.container():
        cols = st.columns(widths)
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if st.session_state.option == "Get Section":
        sub_menu = ["Get by SID", "Get by RID", "Get by CID", "Get by MID", "Get by Semester", "Get by Years", "Get by Capacity", "Get by Capacity Over", "Get by Capacity Under"]
        sub_menu_option = None
        sub_widths = [len(option) for option in sub_menu]

        with st.container():
            cols = st.columns(sub_widths)
            for i, option in enumerate(sub_menu):
                if cols[i].button(option):
                    st.session_state.sub_menu_option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "sub_menu_option" not in st.session_state:
        st.session_state.sub_menu_option = None

    if "sid" not in st.session_state:
        st.session_state.sid = ""

    if "roomid" not in st.session_state:
        st.session_state.roomid = ""

    if "cid" not in st.session_state:
        st.session_state.cid = ""

    if "mid" not in st.session_state:
        st.session_state.mid = ""

    if "semester" not in st.session_state:
        st.session_state.semester = ""

    if "years" not in st.session_state:
        st.session_state.years = ""

    if "capacity" not in st.session_state:
        st.session_state.capacity = ""

    if "set_button" not in st.session_state:
        st.session_state.set_button = False

    def clear():
        st.session_state.sid = ""
        st.session_state.roomid = ""
        st.session_state.cid = ""
        st.session_state.mid = ""
        st.session_state.semester = ""
        st.session_state.years = ""
        st.session_state.capacity = ""
        st.session_state.set_button = False


    def allSections():
        st.header("All Sections")
        try:
            response = requests.get(f"{BASE_URL}/section")
            if response.status_code == 200:
                sections = response.json()

                df = pd.DataFrame(sections)
                df.index = df.index + 1
                st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                st.divider()
                st.divider()
                st.bar_chart(df['semester'].value_counts(), x_label='Sections By Time Given',y_label='Number of Sections', color=(97, 126, 152), height=500)
            else:
                st.error("Failed to fetch sections.")
        except Exception as e:
            st.error(f"An error has occurred: {e}")

    def sectionsBySID():
        st.header("Section by SID")

        val = st.text_input("Room ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.sid = val

        if st.session_state.sid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/{st.session_state.sid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the Section ID")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsByRID():
        st.header("Sections by Room ID")

        val = st.text_input("Room ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.roomid = val

        if st.session_state.roomid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/roomid={st.session_state.roomid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the Room ID")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsByCID():
        st.header("Sections by CID")

        val = st.text_input("Class ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.cid = val

        if st.session_state.cid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/cid={st.session_state.cid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the Class ID")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsByMID():
        st.header("Sections by MID")

        val = st.text_input("Meeting ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.mid = val

        if st.session_state.mid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/mid={st.session_state.mid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the Meeting ID")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsBySemester():
        st.header("Sections by Semester")

        val = st.text_input("Semester:")
        if st.button("Set Semester", type='primary'):
            st.session_state.set_button = True
            st.session_state.semester = val

        if st.session_state.semester:
            try:
                response = requests.get(f"{BASE_URL}/section/semester={st.session_state.semester}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the semester.")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a value.")

    def sectionsByYear():
        st.header("Sections by Year")

        val = st.text_input("Year:")
        if st.button("Set Year", type='primary'):
            st.session_state.set_button = True
            st.session_state.years = val

        if st.session_state.years:
            try:
                response = requests.get(f"{BASE_URL}/section/years={st.session_state.years}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the year.")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a value.")

    def sectionsByCapacity():
        st.header("Sections by Capacity")

        val = st.text_input("Capacity:")
        if st.button("Set Capacity", type='primary'):
            st.session_state.set_button = True
            st.session_state.capacity = val

        if st.session_state.capacity.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/capacity={st.session_state.capacity}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the capacity.")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsByCapacityOver():
        st.header("Sections by Capacity Over")

        val = st.text_input("Capacity:")
        if st.button("Set Capacity", type='primary'):
            st.session_state.set_button = True
            st.session_state.capacity = val

        if st.session_state.capacity.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/capacity:over={st.session_state.capacity}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the capacity.")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    def sectionsByCapacityUnder():
        st.header("Sections by Capacity Under")

        val = st.text_input("Capacity:")
        if st.button("Set Capacity", type='primary'):
            st.session_state.set_button = True
            st.session_state.capacity = val

        if st.session_state.capacity.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}/section/capacity:under={st.session_state.capacity}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame(result)
                        df.index = df.index + 1
                        st.dataframe(df, hide_index=True, height=500, column_order=['sid', 'roomid','cid', 'mid', 'semester', 'years', 'capacity'])
                    else:
                        st.warning("No data found for the capacity.")
                else:
                    st.error(f"Failed to fetch Sections: {response.status_code}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")
        else:
            st.warning("Please enter a number.")

    if st.session_state.option == "All Sections":
        allSections()
    if st.session_state.option == "Get Section":
        match st.session_state.sub_menu_option:
            case "Get by SID":
                clear()
                sectionsBySID()
            case "Get by RID":
                clear()
                sectionsByRID()
            case "Get by CID":
                clear()
                sectionsByCID()
            case "Get by MID":
                clear()
                sectionsByMID()
            case "Get by Semester":
                clear()
                sectionsBySemester()
            case  "Get by Years":
                clear()
                sectionsByYear()
            case "Get by Capacity":
                clear()
                sectionsByCapacity()
            case "Get by Capacity Over":
                clear()
                sectionsByCapacityOver()
            case "Get by Capacity Under":
                clear()
                sectionsByCapacityUnder()

    # if selected_option == "Add Class":
    #     addClass()
    # if selected_option == "Update Class":
    #     updateClass()
    # if selected_option == "DeleteClass":
    #     deleteClass()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")