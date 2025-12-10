import streamlit as st
from dotenv import load_dotenv
import os.path

load_dotenv()
login_path = os.getenv('LOGIN_PATH')
app_path = os.getenv('APP_PATH')

login = st.Page(page = login_path,title= "Login",default=True)
app = st.Page(page = app_path,title = "Copilot")

pages = [
  login,
  app
]


pg = st.navigation(pages,position='sidebar')
pg.run()


