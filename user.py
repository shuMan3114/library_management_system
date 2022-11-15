import numpy as np
import pandas as pd
import getpass
from datetime import date
from passlib.hash import bcrypt
from mailing_user import mail_sender as mail
from format_mail import format_mail
from finances import UFinances

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
        self.membership_level = membership_level
        self.monthlyFees = mem_l_dict[membership_level][0]
        self.maxLimit = mem_l_dict[membership_level][1]
        self.joinDate = date.today()
        self.borrowedList = []
        self.waitlist = []
        self.password = hashed_password
        if(membership_level):
            self.dueDate = np.datetime64(date.today()) + np.timedelta64(1,'M')
        self.paymentDue = UFinances(membership_fees=self.monthlyFees)



    def verify_login(self,entered_password):
        hasher = bcrypt.using(rounds=13)
        verdict = hasher.verify(entered_password, self.password)
        return verdict


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

    def edit_waitlist(self):
        prompts = {
            1: "Enter 1 to add to wailist 2 to remove from waitlist 3 to clear waitlist 4 to exit: ",
            2: "Enter the bookID of the book(s) you wish to remove/add in the form of a list: ",
            3: "Wrong option! Please enter the correct option: ",
            4: "Books removed/added successfully!",
            5: "Waitlist cleared!",
            6: f"Sucssfully exited program! waitlist is: {self.waitlist}"
        }
        option_selected = input(prompts[1])
        while option_selected not in [str(x) for x in range(1,5)]:
            print(prompts[3])
        option_selected = int(option_selected)
        while(option_selected != 4):
            if(option_selected in [1,2]):
                print(self.waitlist)
                book_list = eval(input(prompts[2]))
                if(option_selected == 1):
                    self.waitlist = self.waitlist + book_list
                else:
                    self.waitlist = self.waitlist - book_list
                print(prompts[4])
            elif(option_selected == 3):
                self.waitlist = []
                print(prompts[5])
            
            option_selected = input(prompts[1])
            while option_selected not in [str(x) for x in range(1,5)]:
                print(prompts[3])
            option_selected = int(option_selected)
        
        return prompts[6]
    
    def make_payment(self):
        prompts = {
            1: "Enter 1 to pay all dues 2 to pay membership_fees 3 to pay lost_books 4 to pay part of the total due 5 to exit: ",
            2: "Oops! wrong option entered! "
        }
        print(f"BreakUp : \n{self.paymentDue.print_all()}")
