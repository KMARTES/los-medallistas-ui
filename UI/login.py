import streamlit as st

BASE_URL = "https://los-medallistas-c59825198b5f.herokuapp.com/"

USER = {
    "kmart": "kmart12345",
    "serrano": "serrano12345"
}


def authenticate(username, password):
    return USER.get(username) == password


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Login form
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    def login():
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")


    login_button = st.button("Login", on_click=login, type='primary')

else:
    st.write("Welcome! You are logged in.")
    st.switch_page("../UI/home_page.py")
