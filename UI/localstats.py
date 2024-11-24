import streamlit as st
import pandas as pd
import altair as alt
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
    menu_options = ["Most Capacity", "Most Ratio", "Most Taught / Room", "Most Classes / Semester / Year"]
    selected_option = None

    with st.container():
        cols = st.columns(len(menu_options))
        for i, option in enumerate(menu_options):
            if cols[i].button(option):
                st.session_state.option = option

    if "option" not in st.session_state:
        st.session_state.option = selected_option

    if "building" not in st.session_state:
        st.session_state.building = ""

    if "rid" not in st.session_state:
        st.session_state.rid = ""

    if "year" not in st.session_state:
        st.session_state.year = ""

    if "semester" not in st.session_state:
        st.session_state.semester = ""

    if "fetch_button" not in st.session_state:
        st.session_state.fetch_button = False

    def clear():
        st.session_state.building = ""
        st.session_state.fetch_button = False

    def mostCapacity():
        st.header("Top 3 Rooms with the Most Capacity in the Specified Building")

        val = st.text_input("Enter building name:")

        if st.button("Fetch", type='primary'):
            st.session_state.fetch_button = True
            st.session_state.building = val

            if st.session_state.building:
                try:
                    response = requests.post(f"{BASE_URL}room/{st.session_state.building}/capacity")

                    if response.status_code == 200:
                        result = response.json()

                        if result:
                            df = pd.DataFrame(result)
                            # df.index = df.index + 1
                            df.set_index(df['room_number'], inplace=True)
                            st.dataframe(df, hide_index=True, column_order=['building', 'room_number', 'most_capacity'])
                            st.divider()
                            st.divider()
                            st.bar_chart(df['most_capacity'], x_label='Room Number', y_label='Capacity', color=(2, 35, 89), horizontal=True, height=500)
                        else:
                            st.error("Stat not available.")
                    else:
                        st.error("Failed to fetch requested data.")
                except Exception as e:
                    st.error(f"An error has occurred: {e}")
            else:
                st.error("Please enter a building name. (Must begin with a capital letter.)")


    def mostRatio():
        st.header("Top 3 Rooms with the Most Student-To-Capacity Ratio")

        val = st.text_input("Enter building name:")

        if st.button("Fetch", type='primary'):
            st.session_state.fetch_button = True
            st.session_state.building = val

            if st.session_state.building:
                try:
                    response = requests.post(f"{BASE_URL}room/{st.session_state.building}/ratio")
                    if response.status_code == 200:
                        result = response.json()

                        if result:
                            df = pd.DataFrame(result)
                            df.set_index(df['roomid'], inplace=True)
                            st.dataframe(df, hide_index=True, column_order=['building', 'roomid', 'ratio'])
                            st.divider()
                            st.divider()

                            # Create a sorted DataFrame for charting
                            df_sorted = df.sort_values(by='ratio', ascending=False).head(3)

                            # Create a bar chart with Altair
                            chart = (
                                alt.Chart(df_sorted)
                                .mark_bar()
                                .encode(
                                    y=alt.Y('roomid:N', title='Room Number'),
                                    x=alt.X('ratio:Q', title='Student-to-Capacity Ratio',
                                            scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(tickCount=20)),
                                    color=alt.value('rgb(2,35,89)'),
                                    tooltip=['roomid', 'ratio']
                                )
                                .properties(height=500, width=600)
                            )
                            st.altair_chart(chart, use_container_width=True)
                        else:
                            st.error("Stat not available.")
                    else:
                        st.error("Failed to fetch requested data.")
                except Exception as e:
                    st.error(f"An error has occurred: {e}")
            else:
                st.error("Invalid input.")

    def mostTaughtperRoom():
        st.header("Top 3 Classes that were Taught the Most per Room")

        val = st.text_input("Enter Room ID:")

        if st.button("Fetch", type='primary'):
            st.session_state.fetch_button = True
            st.session_state.rid = val

            if st.session_state.rid.isnumeric():
                try:
                    response = requests.post(f"{BASE_URL}room/{st.session_state.rid}/classes")
                    if response.status_code == 200:
                        result = response.json()

                        if result:
                            df = pd.DataFrame(result)
                            df.set_index(df['cdesc'], inplace=True)
                            st.dataframe(df, hide_index=True, column_order=['cdesc', 'room_number', 'classes_taught'])
                            st.divider()
                            st.divider()
                            st.bar_chart(df['classes_taught'], x_label='Classes per Room', y_label='Classes', color=(2,35,89), horizontal=True, height=500)
                        else:
                            st.error("Stat not available.")
                    else:
                        st.error("Failed to fetch requested data.")
                except Exception as e:
                    st.error(f"An error has occurred: {e}")
            else:
                st.error("Invalid input.")

    def mostClassesperSemesterperYear():
        st.header("Top 3 Most Taught Classes per Semester per Year")

        val1 = st.text_input("Enter Year: Ex: 2022")
        val2 = st.text_input("Enter Semester: Ex: Fall")

        if st.button("Fetch", type='primary'):
            st.session_state.fetch_button = True
            st.session_state.year = val1
            st.session_state.semester = val2

            if st.session_state.year and st.session_state.semester:
                try:
                    response = requests.post(f"{BASE_URL}classes/{st.session_state.year}/{st.session_state.semester}")

                    if response.status_code == 200:
                        result = response.json()

                        if result:
                            df = pd.DataFrame(result)
                            df.set_index(df['cdesc'], inplace=True)
                            st.dataframe(df, hide_index=True, column_order=['cdesc', 'semester', 'years', 'classes_taught'])
                            st.divider()
                            st.divider()
                            st.bar_chart(df['classes_taught'], x_label='Classes Taught', y_label='Classes', color=(2,35,89), horizontal=True, height=500)
                    else:
                        st.error("Failed to fetch requested data.")
                except Exception as e:
                    st.error(f"An error has occurred: {e}")
            else:
                st.error("Invalid input.")

    if st.session_state.option == "Most Capacity":
        clear()
        mostCapacity()
    if st.session_state.option == "Most Ratio":
        clear()
        mostRatio()
    if st.session_state.option == "Most Taught / Room":
        clear()
        mostTaughtperRoom()
    if st.session_state.option == "Most Classes / Semester / Year":
        clear()
        mostClassesperSemesterperYear()
else:
    st.switch_page("../UI/login.py")
