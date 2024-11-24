import streamlit as st

login_page = st.Page("../UI/login.py", title="LOGIN")
logout_page = st.Page("../UI/logout.py", title="LOGOUT")
home_page = st.Page("../UI/home_page.py", title="HOME")
classes_page = st.Page("../UI/classes.py", title="CLASSES")
rooms_page = st.Page("../UI/rooms.py", title="ROOMS")
meetings_page = st.Page("../UI/meetings.py", title="MEETINGS")
requisite_page = st.Page("../UI/requisites.py", title="REQUISITES")
sections_page = st.Page("../UI/sections.py", title="SECTIONS")
localstats_page = st.Page("../UI/localstats.py", title="LOCALSTATS")
globalstats_page = st.Page("../UI/globalstats.py", title="GLOBALSTATS")
chatbot_page = st.Page("../UI/chatbot.py", title="CHATBOT")

pg = st.navigation([login_page, logout_page, home_page, classes_page, rooms_page, meetings_page, requisite_page, sections_page, localstats_page, globalstats_page, chatbot_page], position="hidden")
pg.run()
