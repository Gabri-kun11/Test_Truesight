import streamlit as st  
import re 
import streamlit_authenticator as stauth
import datetime
from deta import Deta

#Database key
DETA_KEY = 'c0cmvcf8u3x_iEwe5zHi6HxtQZeQg53nrpjg4BBWP9nr'

deta = Deta(DETA_KEY)

db = deta.Base('users')

#Create Query
def insert_user(email, username, password):
    
    date_joined = str(datetime.datetime.now())
    
    return db.put({'key': email, 
                   'username': username, 
                   "password": password, 
                   'data_joined': date_joined})

#MANUAL INPUT TO THE DATABASE
#insert_user('samplejsdsds@gmail.com', 'test22323', '123423356')

#Fetching Data
#IMPORTANT FUNCTION
def fetch_user():
    
    users = db.fetch()
    return users.items

#MANUAL CHECKING IF THE DATA IS FETCH FROM THE DATABASE
#print(fetch_user())

def get_user_email():
    
    users = db.fetch()
    email = [] #create row data
    for user in users.items:
        email.append(user['key'])
        
    return email

def get_usernames():
    
    users = db.fetch()
    usernames = [] #create row data
    
    for user in users.items:
        usernames.append(user['key'])
        
    return usernames

#email validation
def validate_email(email):
    
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    
    if re.match(pattern, email):
        return True
    return False

#username validation
def validate_username(username):
    
    pattern = "^[a-zA-Z0-9]*$"
    
    if re.match(pattern, username):
        return True
    return False

def registration():
    
    with st.form(key = 'signup', clear_on_submit= True):
        st.subheader('Sign Up')
        
        #Input boxes
        email = st.text_input('Email', placeholder= 'Enter your Email Address')
        username = st.text_input('Username', placeholder= 'Enter your Username')
        
        password = st.text_input('Password', placeholder= 'Enter your Password', type = 'password')
        confirm_password = st.text_input('Confirm Password', placeholder= 'Confirm your password', type = 'password')
        
        #Validation if the Account is already exist in the database
        if email:
            if validate_email(email):
                if email not in get_user_email():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password) >= 6:
                                    if password == confirm_password:
                                        #pass for testing purposes if the password is match 
                                        hashed_password = stauth.Hasher([confirm_password]).generate()
                                        insert_user(email, username, hashed_password[0])
                                        st.success("Congratulation your account is successfully created")
                                    else: 
                                        st.warning('Password do not match, Please try again')
                                else:
                                    st.warning('Password is too short')
                            else:
                                st.warning('This username is too short, Please Try Again')
                        else:
                            st.warning('This username is already exist')
                    else:
                        st.warning('Invalid username')
                else:
                    st.warning('This Email is already exist')   
            else:
                 st.warning('Invalid email')
        
        st.form_submit_button('Register')
        
#registration()
