import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests




if not firebase_admin._apps:
    cred = credentials.Certificate('kanyarasi-b2617-f793ab6a86db.json')
    firebase_admin.initialize_app(cred)

def app():
    c1,c2,c3 = st.columns(3)


    if "username" not in st.session_state:
        st.session_state.username = ""
    if "useremail" not in st.session_state:
        st.session_state.useremail = ""

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            print('payload sigin',payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    def f():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            global Usernm
            Usernm=(userinfo['username'])
            st.session_state.signedout = False
            st.session_state.logedin = True
            st.session_state.default_index = 1
            st.experimental_rerun()
        except:
            if not st.session_state.get("rerun", True):
                st.warning("Login failed")

    def t():
        st.session_state.signedout = True
        st.session_state.logedin = False
        st.session_state.username = ""
        st.session_state.useremail = ""

    def forget():
        c2.title("Login Page")
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            print(email)
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 
    
    if "signedout" not in st.session_state:
        st.session_state.signedout = True
    if "logedin" not in st.session_state:
        st.session_state.logedin = False

    

    if st.session_state["signedout"]:
        status = c2.selectbox("Login/ Signup",["Login","Signup"])
        email = c2.text_input('Please enter your email')
        password = c2.text_input('Please enter your password',type="password")
        st.session_state.email_input = email
        st.session_state.password_input = password

        if status == "Signup":
            userid = c2.text_input('Please enter your userID')
            if c2.button("Create new account"):
                user = sign_up_with_email_and_password(email=email,password=password,username=userid)
                c2.success("Account created successfully")
                c2.markdown("Please loging using your credentials")

        else:
            login = c2.button("Login", on_click = f)
            


    if st.session_state.logedin:
        c2.title("User Details")
        c2.text("Name:"+ st.session_state.username)
        c2.text("Emailid:"+ st.session_state.useremail)
        c2.button("Sign Out", on_click = t)
