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

    if "cname" "ccode" "cdesc" "term" "years" "cred" "csyllabus" not in st.session_state:
        st.session_state.cname = ""
        st.session_state.ccode = ""
        st.session_state.cdesc = ""
        st.session_state.term = ""
        st.session_state.years = ""
        st.session_state.cred = ""
        st.session_state.csyllabus = ""

    def clear():
        st.session_state.cid = ""
        st.session_state.cname = ""
        st.session_state.ccode = ""
        st.session_state.cdesc = ""
        st.session_state.term = ""
        st.session_state.years = ""
        st.session_state.cred = ""
        st.session_state.csyllabus = ""
        st.session_state.set_button = False


    def allClasses():
        st.header("All Rooms")
        try:
            response = requests.get(f"{BASE_URL}class")
            if response.status_code == 200:
                classes = response.json()

                df = pd.DataFrame(classes)
                df.index = df.index + 1
                st.dataframe(df, hide_index=True, height=500, column_order=['cid', 'cname', 'ccode', 'cdesc', 'term', 'years', 'cred', 'csyllabus'])
                st.divider()
                st.divider()
                st.bar_chart(df['years'].value_counts(), x_label='Time Given', y_label='Number of Classes Given', color=(74, 69, 136), height=500)
            else:
                st.error(f"Failed to fetch Class: {response.status_code} - {response.text}")
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
                response = requests.get(f"{BASE_URL}class/{st.session_state.cid}")

                if response.status_code == 200:
                    result = response.json()

                    if result:
                        df = pd.DataFrame([result])
                        st.dataframe(df, hide_index=True, column_order=['cid', 'cname', 'ccode', 'cdesc', 'term', 'years', 'cred', 'csyllabus'])
                    else:
                        st.warning("No data found for the Room ID")
                else:
                    st.error(f"Failed to fetch Class: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def addClass():
        st.header("Add Class")

        cname = st.text_input("Class Name:")
        ccode = st.text_input("Class Code:")
        cdesc = st.text_input("Class Description:")
        term = st.text_input("Class Term")
        years = st.text_input("Class Year:")
        cred = st.text_input("Class Credits:")
        csyllabus = st.text_input("Class Syllabus Link:")

        if st.button("Add", type='primary'):
            st.session_state.set_button = True
            st.session_state.cname = cname
            st.session_state.ccode = ccode
            st.session_state.cdesc = cdesc
            st.session_state.term = term
            st.session_state.years = years
            st.session_state.cred = cred
            st.session_state.csyllabus = csyllabus

            data = {"cname": cname, "ccode": ccode, "cdesc": cdesc, "term": term, "years": years, "cred": cred, "csyllabus": csyllabus}

        if st.session_state.set_button and st.session_state.cname and st.session_state.ccode and st.session_state.cdesc and st.session_state.term and st.session_state.years and st.session_state.cred and st.session_state.csyllabus:
            try:
                response = requests.post(f"{BASE_URL}class", json=data)

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No data added to Class table.")
                else:
                    st.error(f"Failed to add Class: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def updateClass():
        st.header("Update Class")

        cid = st.text_input("Class ID")
        cname = st.text_input("Class Name:")
        ccode = st.text_input("Class Code:")
        cdesc = st.text_input("Class Description:")
        term = st.text_input("Class Term")
        years = st.text_input("Class Year:")
        cred = st.text_input("Class Credits:")
        csyllabus = st.text_input("Class Syllabus Link:")

        if st.button("Update", type='primary'):
            st.session_state.set_button = True
            st.session_state.cid = cid
            st.session_state.cname = cname
            st.session_state.ccode = ccode
            st.session_state.cdesc = cdesc
            st.session_state.term = term
            st.session_state.years = years
            st.session_state.cred = cred
            st.session_state.csyllabus = csyllabus

            data = {"cid": cid, "cname": cname, "ccode": ccode, "cdesc": cdesc, "term": term, "years": years, "cred": cred, "csyllabus": csyllabus}

        if st.session_state.cid and st.session_state.set_button and st.session_state.cname and st.session_state.ccode and st.session_state.cdesc and st.session_state.term and st.session_state.years and st.session_state.cred and st.session_state.csyllabus:
            try:
                response = requests.put(f"{BASE_URL}class/{st.session_state.cid}", json=data)

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No data added to Class table.")
                else:
                    st.error(f"Failed to update Class: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    def deleteClass():
        st.header("Delete Class by Class ID")

        val = st.text_input("Class ID:")

        if st.button("Delete", type='primary'):
            st.session_state.set_button = True
            st.session_state.cid = val

        if st.session_state.cid:
            try:
                response = requests.delete(f"{BASE_URL}class/{st.session_state.cid}")

                if response.status_code in [200, 201]:
                    result = response.json()

                    if result:
                        st.write(str([result]))
                    else:
                        st.warning("No class ID found.")
                else:
                    st.error(f"Failed to delete Class: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error has occurred: {e}")

    if st.session_state.option == "All Classes":
        allClasses()
    if st.session_state.option == "Get Class":
        clear()
        classByCID()
    if st.session_state.option == "Add Class":
        clear()
        addClass()
    if st.session_state.option == "Update Class":
        clear()
        updateClass()
    if st.session_state.option == "Delete Class":
        clear()
        deleteClass()
else:
    st.session_state.logged_in = False
    st.switch_page("../UI/login.py")
