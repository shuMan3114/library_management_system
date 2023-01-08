from .modules.mailing import send_mail,format_mail
from passlib.hash import bcrypt
import getpass

def pass_input(obj):
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    obj.password = new_pass
    return "Password changed successfully!"

class Admin:

    def __init__(self,admnID,f_name,l_name,contact,hashed_password,cursor,userTable,BooksTable):
        self.admnID = admnID
        self.f_name = f_name
        self.l_name = l_name
        self.contact = contact
        self.password = hashed_password
        self.cursor = cursor
        self.userTable = userTable
        self.booksTable = BooksTable
    
    def add_books(self):
        pass
    def drop_books(self):
        pass
    def edit_books(self):
        pass

    def update_user_dues(self,fees,userID):
        pass

    def delete_user_account(self,userID):
        pass

    def graphing(self):
        pass