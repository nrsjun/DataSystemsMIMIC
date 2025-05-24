import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader



with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def full_logout():
    authenticator.logout()
    st.write("Logging out! bye bye")



return_object = authenticator.login(location='main', key='Login')



if st.session_state.get('authentication_status'):
    authenticator.logout()
    st.write(f'Welcome *{st.session_state.get("name")}*')
    st.title('Welcome to the Streamlit App, here is some data!')
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect!')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')
    st.write("Nah not authenticated....")