import streamlit as st
from streamlit_google_auth import Authenticate

st.set_page_config(
   page_title= "Login",
   layout= "wide",
   initial_sidebar_state= "collapsed"
)

col1, col2 = st.columns([0.4,0.6])

with col1:
  st.markdown("#")
  st.markdown("""<style>
              @import url('https://fonts.googleapis.com/css2?family=Jockey+One&family=Roboto:wght@400;500;700&display=swap');

              .header{
                font-family: 'Jockey One', serif;
                font-size: 120px;
                line-height: 100px;
              }

              </style>""", unsafe_allow_html=True)
  
  st.markdown("<div class = 'header'>UML<br>Copilot</div>", unsafe_allow_html = True)
  
with col2:
  
  st.title("Login")

  
  authenticator = Authenticate(
    secret_credentials_path = 'client_secret.json',
    cookie_name = 'my_cookie_name',
    cookie_key = 'secret_key',
    redirect_uri = 'http://localhost:8501'
  )

  if 'user_info' not in st.session_state:
      st.session_state['user_info'] = None

  authenticator.check_authentification()
  authenticator.login()


# GOOGLE_API_KEY = "AIzaSyD_bJV6tOqGe90tUZfh-6cKNkQWCuC_Yek"
