import streamlit as st
from verify_code import *


#class of Users

class User_id():
    def __init__(self):
        self.list_of_Users=[]
        self.IDD=1
    def add_user(self,first_name,last_name,email):
        user_id = self.IDD
        new_user = input_users(first_name, last_name, email, user_id)
        self.list_of_Users.append(new_user)
        self.IDD += 1 


class input_users():
    def __init__(self,first_name,last_name,email,user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = user_id
        
    

#class of page web
class pages():
    def __init__(self,page_name):
        self.page_name=page_name
    
    def display(self):
        pass

    def go_to(self,page_name):
        st.session_state.page=page_name


class page_home(pages):
    def __init__(self):
        super().__init__("home")
    def display(self):
        col1,col2,col3=st.columns(3)
        col2.title('LINKDIN')
        st.header("Welcome to LINKDIN!")
        first_name = st.text_input("First name:")
        last_name=st.text_input("Last name:")
        email=st.text_input("Email:")

        coll1,coll2,coll3,coll4,coll5,coll6=st.columns(6)
        if coll6.button("Done"):
            if first_name and last_name and email:
                if "users" not in st.session_state:
                    st.session_state.users = User_id()  
                st.session_state.users.add_user(first_name, last_name, email)

                verify=gmail_verify_code()
                verify.send(email)
                st.session_state.verify_code=verify.code
                st.session_state.user_email=email
                self.go_to("page2")
            else:
                st.warning("please fill the information!!")   


class page2(pages):
    def __init__(self):
        super().__init__("page2")
    def display(self):
        col1,col2,col3=st.columns(3)
        col2.title("LINKDIN")
        st.header("verify code was sent your email !! ")
        st.header("Please Enter the code!")
        input_verify_code=st.text_input("Enter Here")
        if st.button("Done"):
            if input_verify_code:
                if (input_verify_code != st.session_state.verify_code0):
                    st.error("verify code is not correct !! please check the email again")
                else:
                    self.go_to("page3")
            else:
                st.warning("please fill the box") #matn ro baad dorost kon
class page3(pages):
    def __init__(self):
        super().__init__("page3")
    def display(self):
        st.title("Hello")


if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    page = page_home()
elif st.session_state.page == "page2":
    page = page2()
elif st.session_state.page == "page3":
    page=page3()

page.display()   


