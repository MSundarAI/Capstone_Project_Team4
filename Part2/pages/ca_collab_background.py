import streamlit as st
import os
st.set_page_config(page_title="background", page_icon="🎹", layout="wide")
st.image('./Part2/images/logo.png', caption = None)
st.write("Current working directory:", os.getcwd())