import streamlit as st
from streamlit_option_menu import option_menu
import register, login, home

#Icon Image

st.set_page_config(
    
    page_icon= "👁", 
    page_title= 'TrueSight'
    
)

#Hide Watermark
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """


st.markdown(hide_streamlit_style, unsafe_allow_html=True)


class multiapp:
    
    def __init__(self):
        self.apps = []
        
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
        
    def run():
    
        with st.sidebar:
            
            #st.sidebar.image("Picture/TrueSight_Logo.png")
            # logo = Image.open("Picture/Truesight_Logo_nobg.png")
            # resize_img = logo.resize((300,300))
            # st.sidebar.image(resize_img)
            
            page = option_menu(
                
                menu_title= "TrueSight",
                options= ["Home", "Signin", "SignUp"],
                icons= ["house", "person-add", "person-dash"],
                menu_icon= "person-bounding-box",
                default_index= 0,
                #orientation= "horizontal",

            ) 
    
        if page == 'Home':
            home.app()
            
        if page == 'Signin':
            login.SignIn()
            
        if page == 'SignUp':
            register.registration()
       

        run()
    
