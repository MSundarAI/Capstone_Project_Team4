import streamlit as st

st.set_page_config(page_title="background", page_icon="🎹", layout="wide")
st.image('images/logo.png', caption = None)
st.write("Current working directory:", os.getcwd())