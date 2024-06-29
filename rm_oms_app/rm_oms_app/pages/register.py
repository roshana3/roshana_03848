import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/"

def register():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["user", "admin"])
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != password2:
            st.error("Passwords do not match")
        else:
            response = requests.post(
                f"{API_URL}/register/",
                json={"username": username, "email": email, "role": role, "password": password}
            )
            if response.status_code == 200:
                st.success("Registration successful")
            else:
                st.error(response.json()["detail"])
