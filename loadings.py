import streamlit as st
from streamlit_lottie import st_lottie
import json
import time

st.set_page_config(page_title="search_loading", layout="centered")

def loading_searching():
    st.markdown("""
    <style>
        .title-text {
            color: #007BFF; /* آبی شیک */
            text-align: center;
            font-size: 60px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

    
    col1,col2,col3=st.columns(3)
    col2.markdown("<div class='title-text'>LINKEDIN</div>", unsafe_allow_html=True)


    def load_lottie_url(file_name: str):
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    
    lottie_loading = load_lottie_url("Animation - 1748614204594 (1).json")
    
    with st.spinner("searching...."):
        st_lottie(lottie_loading, height=200, key="loading")
        time.sleep(2)

    
