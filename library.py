from user import User
from admin import Admin
from book import Book

# - user init has a loop which takes in 
'''
self.UserID = UserID
self.fname = first_name
self.lname = last_name
self.contact = email
self.membership_level = membership_level
'''

def ID_generation(pos,mem_level=0):
    pass
    
def user_init():
    pass

class Library():

    def __init__(self,lib_name,address,postal_code,telephone):
        self.name = lib_name
        self.address = address
        self.postal_code = postal_code
        self.telephone = telephone
        self.userDB = {1 : {}, 2: {}, 3: {}}
        self.adminDict = {}
        self.books = {}
    
    def login(self):
        pompts = {
            1 : "Enter 1 for admin and 2 for user: ",
            2 : "Enter ID: ",
            3 : "Enter password: "
        }

    def sign_up(self):
        pass

