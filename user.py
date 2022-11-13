import numpy as np
import getpass
from datetime import date
from passlib.hash import bcrypt
from mailing_user import mail_sender as mail
from format_mail import format_mail

def pass_input(obj):
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    obj.password = new_pass
    return "Password changed successfully!"

class User:

    def __init__(self,UserID,first_name,last_name,email,membership_level,hashed_password):
        mem_l_dict ={
        0 : [0,1],
        1 : [20,3],
        2 : [40,5],
        3 : [60,7]
    }
        self.UserID = UserID
        self.fname = first_name
        self.lname = last_name
        self.contact = email
        self.monthlyFees = mem_l_dict[membership_level][0]
        self.maxLimit = mem_l_dict[membership_level][1]
        self.joinDate = date.today()
        self.borrowedList = []
        self.waitlist = []
        self.password = hashed_password
        if(membership_level):
            self.paymentDue = self.monthlyFees
            self.dueDate = np.datetime64(date.today()) + np.timedelta64(1,'M')
            self.OverDue = False

    def verify_login(self,entered_password):
        hasher = bcrypt.using(rounds=13)
        verdict = hasher.verify(entered_password, self.password)
        return verdict

    def borrow_book(self,Book):
        if(self.maxLimit - len(self.borrowedList)):
            verdict = Book.update_borrowed_book_status(self.UserID)
            if(verdict):
                self.borrowedList.append(Book.BookID)
                return f"Borrowed Book successfully!"
        else:
            self.waitlist.append(Book.BookID)
            return f""
    
    def return_book(self,Book):
        message = Book.update_returned_book_status()
        if(self.waitlist):
            additional_msg = f"{self.waitlist[0]} can be borrowed!"
        return f"{message}\n{additional_msg}"
    
    def forgot_password(self):
        code = 'alphanumeric_string'
        mail(self.contact,code)
        code_entered = input(f"Enter code sent to {format_mail(self.contact)}: ")
        while code_entered != code:
            code_entered = input(f"Enter code sent to {format_mail(self.contact)}: ")
        return pass_input(self)

    def change_password(self):
        hasher = bcrypt.using(rounds=13)
        pass_entered = getpass(prompt = f"Enter password: ")
        if(hasher.verify(pass_input, self.password)):
            verdict = pass_input(self)
        else:
            verdict = "Wrong password"
        return verdict
