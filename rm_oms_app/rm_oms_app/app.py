import streamlit as st
import requests

# API_URL = "http://backend:8000"

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
                f"{API_URL}/signup/",
                json={"username": username, "email": email, "user_role": role,
                       "password": password, 
                    #    "status":"pending"
                       }
            )
            if response.status_code == 200:
                st.success("Registration successful")
            else:
                st.error(response.json()["detail"])

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):

        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
        data = {
        'grant_type': '',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }
        response = requests.post(f"{API_URL}/login/", headers=headers, data=data)
        # response = requests.post(
        #     f"{API_URL}/login/",
        #     json={"username": email, "password": password}
            
        # )
       
        print("response:", response)
        if response.status_code == 201:
            st.error("Your registration is pending approval")
            
        elif response.status_code == 200:
            token = response.json()["access_token"]
            # user_info = requests.get(f"{API_URL}/users/me/", headers={"Authorization": f"Bearer {token}"})
            user = response.json()["user"]
            # if user_info.status == 200:
            # user = user_info.json()
            st.session_state["token"] = token
            st.session_state["role"] = user["user_role"]
            st.session_state["status"] = user["status"]
            st.session_state["username"] = user["username"]
            if user["status"] == "pending":
                st.warning("Your request is pending approval.")
            elif user["user_role"] == "admin":
                # admin_dashboard1()
                show_admin_dashboard()
            else:
                user_dashboard()
            # else:
            #     st.error("Your registration is pending approval")
        else:
            st.error("Invalid credentials login")

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
                        f"{API_URL}/approve_user/{user['email']}",
                        headers={"Authorization": f"Bearer {st.session_state['token']}"}
                    )
                    if approve_response.status_code == 200:
                        st.success(f"User {user['username']} approved")
                        # st.experimental_rerun()
                    else:
                        st.error(f"Failed to approve {user['username']}")

def admin_dashboard1():
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state['username']}")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

        if password != password2:
            st.error("Passwords do not match")
        else:
            response = requests.post(
                f"{API_URL}/signup/",
                json={"username": username, "email": email, "user_role": role,
                       "password": password, 
                    #    "status":"pending"
                       }
            )
            if response.status_code == 200:
                st.success("Registration successful")
            else:
                st.error(response.json()["detail"])


def user_dashboard():
    st.title("User Dashboard")
    st.write(f"Welcome, {st.session_state['username']}")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
    st.write("This is the user dashboard.")


# # Page routing
# if "page" not in st.session_state:
#     st.session_state["page"] = "login"

# if st.session_state["page"] == "login":
#     show_login_page()
# elif st.session_state["page"] == "admin_dashboard":
#     show_admin_dashboard()

def show_admin_dashboard():
    token = st.session_state.get("token")
    if not token:
        st.error("You need to login first")
        return

    st.title("Admin Dashboard")
    users = get_users(token)
    for user in users:
        st.write(f"Name: {user['username']}, Email: {user['email']}, Status: {user['status']}")
        if user['status'] == 'pending':
            if st.button(f"Approve {user['username']}"):
                if approve_user(user['email'], token):
                    st.success(f"User {user['username']} approved")
                else:
                    st.error(f"Failed to approve user {user['username']}")


# Create a function to get the list of users
def get_users(token):
    response = requests.get(f"{API_URL}/users/", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return response.json()
    return []

# Create a function to approve a user
def approve_user(username, token):
    response = requests.post(f"{API_URL}/approve_user/${username}", headers={"Authorization": f"Bearer {token}"})
    return response.status_code == 200

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Register"])
    
    if page == "Login":
        login()
    elif page == "Register":
        register()
 
if __name__ == "__main__":
    main()
