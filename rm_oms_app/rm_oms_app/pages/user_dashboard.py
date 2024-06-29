import streamlit as st

def user_dashboard():
    st.title("User Dashboard")
    st.write(f"Welcome, {st.session_state['username']}")
    st.write("This is the user dashboard.")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
