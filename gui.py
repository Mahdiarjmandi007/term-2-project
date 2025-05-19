import streamlit as st

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

        if st.button("Done"):
            if first_name and last_name and email:
                if "users" not in st.session_state:
                    st.session_state.users = User_id()  
                st.session_state.users.add_user(first_name, last_name, email)
                self.go_to("page2")
            else:
                st.warning("please fill the information!!")   


class page2(pages):
    def __init__(self):
        super().__init__("page2")
    def display(self):
        st.write("salam")       

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    page = page_home()
elif st.session_state.page == "page2":
    page = page2()

page.display()   


