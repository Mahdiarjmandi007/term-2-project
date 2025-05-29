import random
import yagmail

class gmail_verify_code():
    def __init__(self):
        self.code=None
        self.email=None
    def creat_code(self):
        code=str(random.randint(100000,999999))
        return code
    def send(self,email):
        self.eamil=email
        self.code=self.creat_code()
        yag=yagmail.SMTP("arjmandipython@gmail.com","yydt soiw vyhr izny")
        yag.send(to=email, subject="Verification Code", contents=f"Your code is: {self.code}")