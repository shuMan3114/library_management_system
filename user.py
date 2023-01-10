import numpy as np
import getpass
from datetime import date
from passlib.hash import bcrypt
from modules.options import optionValidator,pass_input


class User:

    def __init__(self,userDf):
        self.UserID = userDf['UserID'][0]
        self.fname = userDf['first_name'][0]
        self.lname = userDf['last_name'][0]
        self.contact = userDf['email'][0]
        self.borrowedList = userDf['borrowedList'][0]
        self.wishlist = userDf['wishlist'][0]
        self.password = userDf['hashed_password'][0]
    

    def borrow_book(self,Book):
        verdict = Book.update_borrowed_book_status()
        if(verdict):
            borrowBooks = eval(self.borrowedList)
            borrowBooks.append(Book.BookID)
            self.borrowedList = str(borrowBooks)
            print("Borrowed Book successfully!")
            return 1
        else:
            print("Book list is full! Please consider adding book to wishlist")
            return -2
    

    def return_book(self,Book):
        message = Book.update_returned_book_status()
        print("Book returned successfully! ")


    def edit_wishlist(self):
        wihslist = eval(self.wishlist)
        prompts = {
            1: "Enter 1 to add to wishlist 2 to remove from wishlist 3 to clear wishlist 4 to exit: ",
            2: "Enter the bookID of the book(s) you wish to remove/add in the form of a list: ",
            3: "Book(s) removed/added successfully!",
            4: "wishlist cleared!",
            5: f"Sucssfully exited program! wishlist is: {wihslist}"
        }
        option_selected = optionValidator(prompts[1],lower_limit=1,higher_limit=4)
        while(option_selected != 4):
            if(option_selected in [1,2]):
                print(wihslist)
                book_list = eval(input(prompts[2]))
                if(option_selected == 1):
                    wihslist = wihslist + book_list
                else:
                    wihslist = wihslist - book_list
                print(prompts[3])
            elif(option_selected == 3):
                self.wishlist = []
                print(prompts[4])
            
            option_selected = optionValidator(prompts[1],lower_limit=1,higher_limit=4)
        self.wishlist = str(wihslist)
        return prompts[5]