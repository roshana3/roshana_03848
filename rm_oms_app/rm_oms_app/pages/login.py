import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/"


def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = requests.post(
            f"{API_URL}/token",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            user_info = requests.get(f"{API_URL}/users/me/", headers={"Authorization": f"Bearer {token}"})
            if user_info.status_code == 200:
                user = user_info.json()
                st.session_state["token"] = token
                st.session_state["role"] = user["role"]
                st.session_state["status"] = user["status"]
                st.session_state["username"] = user["username"]
                if user["status"] == "pending":
                    st.warning("Your request is pending approval.")
                elif user["role"] == "admin":
                    st.experimental_rerun()
                else:
                    st.experimental_rerun()
            else:
                st.error("Failed to retrieve user information.")
        else:
            st.error("Invalid credentials")
