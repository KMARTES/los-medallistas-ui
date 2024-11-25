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
    menu_options = ["All Rooms", "Get Room", "Add Room", "Update Room", "Delete Room"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "rid" not in st.session_state:
        st.session_state.rid = ""

    if "set_button" not in st.session_state:
        st.session_state.set_button = False

    if "building" "room_number" "capacity" not in st.session_state:
        st.session_state.building = ""
        st.session_state.room_number = ""
        st.session_state.capacity = ""

    def clear():
        st.session_state.rid = ""
        st.session_state.building = ""
        st.session_state.room_number = ""
        st.session_state.capacity = ""
        st.session_state.set_button = False


    def allRooms():
        st.header("All Rooms")
        try:
            response = requests.get(f"{BASE_URL}room")
            if response.status_code == 200:
                rooms = response.json()

                df = pd.DataFrame(rooms)
                df.index = df.index + 1
                st.dataframe(df, hide_index=True, height=500, column_order=['rid', 'building', 'room_number', 'capacity'])
                st.divider()
                st.divider()
                st.bar_chart(df['building'].value_counts(), x_label='Rooms in Buildings', y_label= 'Number of Rooms', color= (234, 200, 120), horizontal= False)

            else:
                st.error(f"Failed to fetch Rooms: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error has occurred: {e}")


    def roomByRID():
        st.header("Get Room by Room ID")
        val = st.text_input("Room ID:")
        if st.button("Set ID", type='primary'):
            st.session_state.set_button = True
            st.session_state.rid = val

        if st.session_state.rid.isnumeric():
            try:
                response = requests.get(f"{BASE_URL}room/{st.session_state.rid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        df.index = df.index + 1
                        st.divider()
                        st.divider()
                        st.dataframe(df, hide_index=True, height=500)
                    else:
                        st.warning("No data found for the Room ID")
                else:
                    st.error(f"Failed to fetch Room: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def addRoom():
        st.header("Add Room")

        building = st.text_input("Building:")
        room_number = st.text_input("Room Number:")
        capacity = st.text_input("Room Capacity:")

        if st.button("Add", type='primary'):
            st.session_state.building = building
            st.session_state.room_number = room_number
            st.session_state.capacity = capacity
            st.session_state.set_button = True

            data = {"building": building, "room_number": room_number, "capacity": capacity}

        if st.session_state.building and st.session_state.room_number and st.session_state.capacity:
            try:
                response = requests.post(f"{BASE_URL}room", json=data)

                if response.status_code in [200,201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No data added to Room table.")
                else:
                    st.error(f"Failed to add Room: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occured: {e}")

    def updateRoom():
        st.header("Update Room")

        rid = st.text_input("Room ID:")
        building = st.text_input("Building:")
        room_number = st.text_input("Room Number:")
        capacity = st.text_input("Room Capacity:")

        if st.button("Update", type='primary'):
            st.session_state.rid = rid
            st.session_state.building = building
            st.session_state.room_number = room_number
            st.session_state.capacity = capacity
            st.session_state.set_button = True

            data = {"rid": rid, "building": building, "room_number": room_number, "capacity": capacity}

        if st.session_state.rid and st.session_state.building and st.session_state.room_number and st.session_state.capacity:
            try:
                response = requests.put(f"{BASE_URL}room/{st.session_state.rid}", json=data)

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No data added to Room table.")
                else:
                    st.error(f"Failed to update Room: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occured: {e}")

    def deleteRoom():
        st.header("Delete Room by Room ID")

        val = st.text_input("Room ID:")

        if st.button("Delete", type='primary'):
            st.session_state.rid = val
            st.session_state.set_button = True

        if st.session_state.rid:
            try:
                response = requests.delete(f"{BASE_URL}room/{st.session_state.rid}")

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No room ID found.")
                else:
                    st.error(f"Failed to delete Room: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Rooms":
        allRooms()
    if st.session_state.option == "Get Room":
        clear()
        roomByRID()
    if st.session_state.option == "Add Room":
        clear()
        addRoom()
    if st.session_state.option == "Update Room":
        clear()
        updateRoom()
    if st.session_state.option == "Delete Room":
        clear()
        deleteRoom()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")