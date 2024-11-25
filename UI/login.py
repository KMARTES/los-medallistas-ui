import streamlit as st
import requests

BASE_URL = "https://streamlit-for-medallistas-e611ec6e2503.herokuapp.com/login"

def authenticate(username, password):
    data = {"username": username, "password": password}
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 200:
        return True
    else:
        return False


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
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
