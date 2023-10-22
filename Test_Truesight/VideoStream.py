import streamlit as st
from streamlit_webrtc import webrtc_streamer

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown("---")

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: white;'>Video Stream</p>", unsafe_allow_html=True)
webrtc_streamer(key="sample")

st.markdown("---")