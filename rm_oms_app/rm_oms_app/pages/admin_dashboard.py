import streamlit as st
import requests

API_URL = "http://backend:8000"
# API_URL = "http://127.0.0.1:8000/"


def admin_dashboard():
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state['username']}")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    response = requests.get(f"{API_URL}/admin/users/", headers={"Authorization": f"Bearer {st.session_state['token']}"})
    if response.status_code == 200:
        users = response.json()
        for user in users:
            st.write(f"Email: {user['email']}, Name: {user['username']}, Status: {user['status']}")
            if user['status'] == 'pending':
                if st.button(f"Approve {user['username']}"):
                    approve_response = requests.post(
                        f"{API_URL}/admin/users/{user['id']}/approve/",
                        headers={"Authorization": f"Bearer {st.session_state['token']}"}
                    )
                    if approve_response.status_code == 200:
                        st.success(f"User {user['username']} approved")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to approve {user['username']}")
