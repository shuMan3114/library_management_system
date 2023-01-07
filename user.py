import numpy as np
import getpass
from datetime import date
from passlib.hash import bcrypt
from .modules.mailing import send_mail,format_mail


# refactor this part -- create dir <modules> -- place in file pass_management
def pass_input(obj):
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    obj.password = new_pass
    return "Password changed successfully!"


# refactor this too -- > place in file input_management
def option_validator(prompt,lower_limit,higher_limit):
    option_selected = input(prompt)
    while option_selected not in [str(x) for x in range(lower_limit,higher_limit+1)]:
        print("Wrong Option! Please retry")
    option_selected = int(option_selected)
    return option_selected
    

class User:

    def __init__(self,userDf):
        self.UserID = userDf['UserID'][0]
        self.fname = userDf['first_name'][0]
        self.lname = userDf['last_name'][0]
        self.contact = userDf['email'][0]
        self.joinDate = date.today()
        self.borrowedList = []
        self.wishlist = []
        self.password = userDf['hashed_password'][0]
        self.dues = 0

    def borrow_book(self,Book):
        verdict = Book.update_borrowed_book_status(self.UserID)
        if(verdict):
            self.borrowedList.append(Book.BookID)
            return f"Borrowed Book successfully!"
    

    def return_book(self,Book):
        message = Book.update_returned_book_status()
        if(self.wishlist):
            additional_msg = f"{self.wishlist[0]} can be borrowed!"
        return f"{message}\n{additional_msg}"

    def edit_wishlist(self):
        prompts = {
            1: "Enter 1 to add to wishlist 2 to remove from wishlist 3 to clear wishlist 4 to exit: ",
            2: "Enter the bookID of the book(s) you wish to remove/add in the form of a list: ",
            3: "Book(s) removed/added successfully!",
            4: "wishlist cleared!",
            5: f"Sucssfully exited program! wishlist is: {self.wishlist}"
        }
        option_selected = option_validator(prompts[1],1,4)
        while(option_selected != 4):
            if(option_selected in [1,2]):
                print(self.wishlist)
                book_list = eval(input(prompts[2]))
                if(option_selected == 1):
                    self.wishlist = self.wishlist + book_list
                else:
                    self.wishlist = self.wishlist - book_list
                print(prompts[3])
            elif(option_selected == 3):
                self.wishlist = []
                print(prompts[4])
            
            option_selected = option_validator(prompts[1],1,4)
        
        return prompts[5]