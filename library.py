from user import User
from admin import Admin
from book import Book
from datetime import date
import pandas as pd
import pyodbc
import getpass
from passlib.hash import bcrypt
import mysql.connector as m
import sql_functions as sql
from modules.options import optionValidator,pass_input,ID_generation



class Library():

    def __init__(self,lib_name,address,postal_code,telephone,cursor,cnx,userTable,adminTable,booksTable,seeds=None):
        tdate = date.today()

        self.name = lib_name
        self.address = address
        self.postal_code = postal_code
        self.telephone = telephone
        self.cursor = cursor
        self.cnx = cnx
        self.userTable = userTable
        self.adminTable = adminTable
        self.booksTable = booksTable
        if(seeds == None):
            self.Useed = 'U'+str(tdate.year)+'0000'
            self.Aseed = 'A'+str(tdate.year)+'0000'
            self.Bseed = 'B'+str(tdate.year)+'0000'
        else:
            self.Useed = 'U'+str(tdate.year)+seeds[0][5:]
            self.Aseed = 'A'+str(tdate.year)+seeds[1][5:]
            self.Bseed = 'B'+str(tdate.year)+seeds[2][5:]
    

    def login_signUp(self):
        hasher = bcrypt.using(rounds=13)
        tdate = date.today()
        prompts = {
            1 : "Enter 1 to login and 2 to sign up 3 to exit: ",
            2 : "Enter 1 for admin and 2 for user: ",
            3 : "Enter ID: ",
            4 : "Enter password: ",
            5 : "User does not exist! Please SignUp!",
            6 : "Incorrect Username or password!",
            7 : "Enter first name: ",
            8 : "Enter last name: ",
            9 : "Enter contact: ",
            10 : "Re-enter new password: ",
            11 : "Passwords do not match!: ",
            12 : "User already exists please login!: "
        }
        verdict = optionValidator(prompts[1],lower_limit=1,higher_limit=2)
        if(verdict in [0,3]):
            return 0
        elif(verdict == 1):
            level = optionValidator(prompts[2],lower_limit=1,higher_limit=2)
            if(not level):
                return -2
            ID = input(prompts[3])
            if(level == 1):
                search_result = sql.select(self.cnx,['*'],self.adminTable,f"admnID = '{ID}'",printable=0)
            else:
                search_result = sql.select(self.cnx,['*'],self.userTable,f"UserID = '{ID}'",printable=0)
            if(len(search_result)):
                password = hasher.hash(getpass.getpass(prompts[4]))
                verdict = optionValidator(prompts[4],error_prompt=prompts[6],check_value=search_result.password[0])
                if(verdict == password):
                    print("Log in success!")
                    if(level == 1):
                        cur_user = Admin(search_result,self.cursor,self.cnx,self.userTable,self.booksTable)
                    else:
                        cur_user = User(search_result)
                    return [level,cur_user]
                else:
                    return -2
            else:
                print(prompts[5])
                return -2
        else:
            emptyDf = pd.DataFrame()
            level = optionValidator(prompts[2],lower_limit=1,higher_limit=2)
            if(not level):
                return -2
            f_name = input(prompts[7])
            l_name = input(prompts[8])
            contact = input(prompts[9])
            if(level == 1):
                ID = ID_generation(self.Aseed)
                extra_fields = 0
                search_result = sql.select(self.cnx,['*'],self.adminTable,f"contact = '{contact}'",printable=0)
            else:
                ID = ID_generation(self.Useed)
                extra_fields = ["'[]'","'[]'"]
                search_result = sql.select(self.cnx,['*'],self.userTable,f"contact = '{contact}'",printable=0)
            if(len(search_result)):
                print(prompts[12])
                return -2
            new_pass = pass_input()
            if(extra_fields != 0):
                insert_vals = [f"'{ID}'",f"'{f_name}'",f"'{l_name}'",f"'{contact}'",f"'{new_pass}'"] + extra_fields
            else:
                insert_vals = [f"'{ID}'",f"'{f_name}'",f"'{l_name}'",f"'{contact}'",f"'{new_pass}'"]
            if(level ==1):
                sql.insert(self.cursor,self.adminTable,values=0,record_df=emptyDf,single_value=True,value_list=insert_vals)
                cur_user = Admin(sql.select(self.cnx,['*'],self.adminTable,f"admnID = '{ID}'",printable=0),self.cursor,self.cnx,self.userTable,self.booksTable)
                self.Aseed = ID
            else:
                sql.insert(self.cursor,self.userTable,values=0,record_df=emptyDf,single_value=True,value_list=insert_vals)
                cur_user = User(sql.select(self.cnx,['*'],self.userTable,f"UserID = '{ID}'",printable=0))
                self.Useed = ID
            print("Sign Up Process complete!")
            return [level,cur_user]


    def searchBooks(self):
        attribute_db = ['BookID','name','author','ISBN','publication','genre','times_borrowed','unavailable']
        prompts = {
            1 : "\n".join([str(x)+' for '+ attribute_db[x] for x in range(len(attribute_db))]),
            3 : "Enter the parameter number in a list with the parameter: ",
            4 : "Enter the subcategory/ies in the form of a list: ",
            5 : "Enter BookIDS of books you wish to use later if none enter [-1]: ",
            6 : "Looks like the book is unavailable: "
        }
        print(prompts[1])
        param_selected = int(eval(input(prompts[3])))
        if(param_selected in range(len(attribute_db))):
            if(param_selected not in [0,1,3]):
                distinct_vals = sql.select(self.cnx,[f'DISTINCT {attribute_db[param_selected]}'],self.booksTable,printable=0)
                print(distinct_vals)
                subcats = eval(input(prompts[4]))
                for subcat in subcats:
                    val = distinct_vals.iloc[subcat,0]
                    sql.select(self.cnx,['*'],self.booksTable,f"{attribute_db[param_selected]} = '{val}'",order_by='times_borrowed',desc = True)
            else:
                approx_string = input("Enter a keyword/ID/ISBN: ")
                result = sql.select(self.cnx,['*'],self.booksTable,f'{attribute_db[param_selected]} LIKE "%{approx_string}%"',printable=0)
                print(result)
            books_selected = eval(input(prompts[5]))
            if(books_selected[0] == -1):
                return []
            else:
                books_selected = [f"'{x.upper()}'" for x in books_selected]
                sql.select(self.cnx,['*'],self.booksTable,f'BookID IN (""{",".join(books_selected)})')
                return books_selected
        else:
            print("Wrong option!!")
            return -1
    

    def display_gen_information(self):
        genInfo = {
            'name' : self.name,
            'address' : self.address,
            'telephone' : self.telephone,
            'postal code' : self.postal_code,
            'Number of Books' : int(self.Bseed[5:]),
            'Number of Users' : int(self.Useed[5:]),
            'Number of Admins' : int(self.Aseed[5:])
        };
        for key,val in genInfo.items():
            print(f'{key} : {val}')

    def user_loop(self,User):
        prompts = {
            1 : "Enter 1 to borrow a book\nEnter 2 to return a book\nEnter 3 to search for a book\nEnter 4 to update credentials or pay dues\nEnter 5 to edit wishlist\nEnter 6 to logout: ",
            2 : "Enter 1 to use the result of the search query and 2 to enter BOOKID: ",
            3 : "Enter BOOKID(s)(as a list)(enter - [-1] to escape): ",
            4 : "Thank you for using the library!",
            5 : "Enter 1 to search for a book and 2 to directly borrow/return: ",
            6 : "Enter 1 to add to wishlist or 2 to continue: ",
            7 : "Enter choice: ",
            8 : "Enter new attr: "
        }
        temp_list = []
        while True :
            print(prompts)
            option = optionValidator(prompts[1],lower_limit=1,higher_limit=6)
            if(option == 0):
                pass
            elif(option == 6):
                print(prompts[4])
                sql.update(self.cursor,self.cnx,self.userTable,list(User.__dict__.keys()),[f"'{str(x)}'" for x in list(User.__dict__.values())],f'ID = "{User.UserID}"')
                return 1
            elif(option in [1,2]):
                optionsDict = {
                    1 : User.borrow_book(),
                    2 : User.return_book()
                }
                if(temp_list):
                    path = optionValidator(prompts[2],lower_limit=1,higher_limit=2)
                    if(not path):
                        pass
                    elif(path == 1):
                        print(*temp_list,sep="\n")
                    b_list = eval(prompts[3])
                    if(b_list[0] == -1):
                        pass
                    for b in b_list:
                        new_book = Book(sql.select(self.cnx,['*'],self.booksTable,f"bookID = '{b}'"))
                        verdict = optionsDict[option](new_book)
                        if(verdict == -2):
                            u_input = optionValidator(prompts[6],lower_limit=1,higher_limit=2)
                            if(u_input == 1):
                                User.edit_wishlist()
                else:
                    print("No previous search query exists!")
                    b_list = eval(prompts[3])
            elif(option in [3,5]):
                if(option == 3):
                    temp_list = self.searchBooks()
                    if(temp_list == -1):
                        print("temp_list reverted to being empty!")
                        temp_list = []
                else:
                    User.edit_wishlist()
            else:
                attrs = ['f_name','l_name','contact','password']
                for x in range(len(attrs)):
                    print(f'{x} for {attrs[x]}')
                attr_no = optionValidator(prompts[7],lower_limit=0,higher_limit=3)
                if(attr_no == -1):
                    pass
                elif(attr_no== 3):
                    User.password = pass_input()
                else:
                    new_Attr = input(prompts[8])
                    if(attr_no == 0):
                        User.f_name = new_Attr
                    elif(attr_no == 1):
                        User.l_name = new_Attr
                    else:
                        User.contact = new_Attr
            

    def admin_loop(self,Admin):
        prompts = {
            1 : "Enter 1 to plot graphs\nEnter 2 to Remove User\nEnter 3 to manage books\nEnter 4 to add a book\n5 to log out: ",
            2 : "Enter 1 to Search for Book(s) and 2 to enter directly: ",
            3: "Enter UserID: ",
            4 : "Enter the details of a new book as a list: ",
            5 : "Enter bookID to manage: ",
            6 : "Successfully logged out!"
        }
        while True:
            choice = optionValidator(prompts[1],lower_limit=1,higher_limit=5)
            if(choice == 5):
                print(prompts[6])
                return
            elif(choice == 0):
                pass
            elif(choice == 1):
                Admin.graphing()
            elif(choice == 2):
                user = input(prompts[3])
                Admin.delete_user_account(user)
            elif(choice == 3):
                book = input(prompts[5])
                Admin.edit_books(book)
            else:
                book_list = eval(input(prompts[4]))
                sql.insert(self.cursor,self.booksTable,pd.DataFrame(),single_value=True,value_list=book_list)
    
    def main_loop(self):
        prompts = {
            1 : "Welcome to library!\nEnter 1 to login/sign-up\nEnter 2 to search for books\nEnter 3 to display general information\nEnter 4 to exit: ",
            2 : "Thank you for using the library!"
        }
        temp_list = []
        while True:
            choice = optionValidator(prompts[1],lower_limit=1,higher_limit=4)
            if(choice in [0,4]):
                print(prompts[2])
                break
            elif(choice == 1):
                CurUser = self.login_signUp()
                if(CurUser == 0):
                    pass
                elif(CurUser == -2):
                    CurUser = self.login_signUp()
                else:
                    if(CurUser[0] == 1):
                        self.admin_loop(CurUser[1])
                    else:
                        self.user_loop(CurUser[1])
            elif(choice == 2):
                temp_list = self.searchBooks()
            elif(choice == 3):
                self.display_gen_information()




#database connection
cnx = m.connect(user='root', password='student',host='localhost',database='LIBRARY')
cursor = cnx.cursor() 



b = 'books'
u = 'User'
a = 'Admin'
library = Library('ganesh','#25,23','560072','080-1234567',cursor,cnx,u,a,b)
library.main_loop()