import streamlit as st
from verify_code import *
from loadings import ss,loading_searching
from data_mine import *
import pandas as pd
import threading




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
        col2.title("LINEKDIN")
        st.header("verify code was sent your email!!")
        st.header("please enter the code ")
        input_code=st.text_input("Enter Here")
        if st.button("done"):
            if input_code:
                if (input_code != st.session_state.verify_code):
                    st.error("verify code is not correct !! \n please check the email")
                else :
                    self.go_to("page3")
            else:
                st.warning("please fill the box") #matn ro baad dorost kon
             
class page3(pages):
    def __init__(self):
        super().__init__("page3")
        self.job_searched=""
        self.lacation=""
    def display(self):
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
        with col2:
            col2.markdown("<div class='title-text'>LINKEDIN</div>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)   
        coll1,coll2,coll3=st.columns(3)
        with coll1:
            self.job_searched=coll1.text_input("Search jobs:",placeholder="search Here.....")
            self.location=coll1.text_input("location:",placeholder="Here.....")
            if st.button("done"):
                if self.job_searched and self.location:
                    st.session_state.job_searched = self.job_searched
                    st.session_state.location = self.location
                    st.session_state.loading_page = page_loadings(self.job_searched,self.location)
                    self.go_to("page_loading")
                else:
                    st.warning("please fill the boxes")
class page_loadings(pages):
    def __init__(self,job_searched,location):
        super().__init__("page_loading")
        self.job_searched = job_searched
        self.location = location
    def display(self):
        st.markdown("## ⏳ Mining data from LinkedIn... Please wait.")

        if not st.session_state.get("mining_started", False):
            def mine_data():
                bot = DT_MINE()
                bot.run(self.job_searched, self.location)
            thread = threading.Thread(target=mine_data)
            thread.start()
            st.session_state.mining_started = True
        if st.button("Show Job Results"):
                st.session_state.page = "page4"
                st.rerun()
        
        
class page4(pages):
    def __init__(self):
        super().__init__("page4")
    def display(self):
        for key in ["data_mined", "job_searched", "location", "loading_page"]:
            st.session_state.pop(key, None)
        st.title("🔍 Job Results")
        
        try:
            df = pd.read_csv("jobs.csv")
            st.dataframe(df, use_container_width=True)
        except FileNotFoundError:
            st.error("error to read file")


if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    page = page_home()
elif st.session_state.page == "page2":
    page = page2()
elif st.session_state.page == "page3":
    page=page3()
elif st.session_state.page=="page4":
    page=page4()
elif st.session_state.page=="page_loading":
    job = st.session_state.get("job_searched", "")
    loc = st.session_state.get("location", "")
    page = page_loadings(job, loc)  

page.display()   


