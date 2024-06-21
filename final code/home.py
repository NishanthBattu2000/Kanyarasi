import streamlit as st
from streamlit_option_menu import option_menu
import account, datainput, editdata

class MultiApp:
    st.set_page_config(layout="wide")
    def __init__(self):
        self.apps = []
        if "default_index" not in st.session_state:
            st.session_state.default_index = 0
        

    def add_app(self, title, function):
        self.app.append({
            "title": title,
            "function": function
        })
    def run(self):
        with st.sidebar:
            st.image("logo_ata.webp")
            app = option_menu(
                menu_title="Select Options",
                options=["Account","Data entry", "Edit data"],
                icons=['person-circle','house-fill','pen'],
                default_index=st.session_state.default_index,
                styles={
                    "container": {"padding": "5!important","background-color":'white'},
        "icon": {"color": "black", "font-size": "16px"}, 
        "nav-link": {"color":"black","font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "skyblue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
            )
        if app == "Account":
            account.app()
        if app == "Data entry":
            datainput.app()
        if app == "Edit data":
            editdata.app()
multi_app = MultiApp()
multi_app.run()



