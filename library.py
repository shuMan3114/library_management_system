from user import User
from admin import Admin
from book import Book
from datetime import date
import sql_functions as sql
import getpass
from passlib.hash import bcrypt


def pass_input():
    new_password = getpass.getpass(prompt="Enter new password: ")
    re_entered_pass = getpass.getpass(prompt="Re-enter new password: ")
    while new_password != re_entered_pass:
        re_entered_pass = getpass.getpass(prompt="Incorrect! Passwords do not match! Re-enter: ")
    hasher = bcrypt.using(rounds=13)
    new_pass = hasher.hash(new_password)
    return new_pass


def optionValidator(prompt,escape_pormpt="Return",error_prompt="Wrong Option",lower_limit=None,higher_limit=None,check_value=None):
    if(lower_limit == None):
        menu_choice = -1
    else:
        menu_choice = lower_limit - 1
    new_prompt = prompt + f'Enter {menu_choice} to {escape_pormpt}'   
    if(lower_limit != None):
        option_selected = input(prompt)
        while option_selected not in [str(x) for x in range(lower_limit -1 , higher_limit + 1)]:
            print(error_prompt)
            option_selected = input(new_prompt)
        return int(option_selected)
    else:
        option_selected = input(prompt)
        while option_selected != str(check_value) or option_selected != str(menu_choice):
            print(error_prompt)
            option_selected = input(new_prompt)
        return option_selected


def ID_generation(seed):
    num = int(seed[5:])
    num += 1
    padding = len(str(num))%4
    if(padding):
        num = "".join((4-padding)*['0']) + str(num)
    else:
        num = str(num)
    return num


class Library():

    def __init__(self,lib_name,address,postal_code,telephone,cursor,userTable,adminTable,booksTable,seeds=None):
        tdate = date.today()

        self.name = lib_name
        self.address = address
        self.postal_code = postal_code
        self.telephone = telephone
        self.cursor = cursor
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
            1 : "Enter 1 to login and 2 to sign up: ",
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
        if(not verdict):
            return -1
        elif(verdict == 1):
            level = optionValidator(prompts[2],lower_limit=1,higher_limit=2)
            if(not level):
                return -2
            ID = input(prompts[3])
            if(level == 1):
                search_result = sql.select(self.cursor,['*'],self.adminTable,f"ID = '{ID}'",print=0)
            else:
                search_result = sql.select(self.cursor,['*'],self.userTable,f"ID = '{ID}'",print=0)
            if(search_result):
                password = hasher.hash(getpass.getpass(prompts[4]))
                verdict = optionValidator(prompts[4],error_prompt=prompts[6],check_value=search_result.password)
                if(verdict == password):
                    print("Log in success!")
                    cur_user = User(search_result)
                    return [cur_user]
                else:
                    return -2
            else:
                print(prompts[5])
                return -2
        else:
            level = optionValidator(prompts[2],lower_limit=1,higher_limit=2)
            if(not level):
                return -2
            f_name = input(prompts[7])
            l_name = input(prompts[8])
            contact = input(prompts[9])
            if(level == 1):
                ID = ID_generation(self.Aseed)
                extra_fields = [[],[],0]
                search_result = sql.select(self.cursor,['*'],self.adminTable,f"contact = '{contact}'",print=0)
            else:
                ID = ID_generation(self.Useed)
                extra_fields = []
                search_result = sql.select(self.cursor,['*'],self.userTable,f"contact = '{contact}'",print=0)
            if(search_result):
                print(prompts[12])
                return -2
            new_pass = pass_input()
            insert_vals = [f"'{ID}'",f"'{f_name}'",f"'{l_name}'",f"'{contact}'",f"'{new_pass}'"] + extra_fields
            if(level ==1):
                sql.insert(self.cursor,self.adminTable,single_value=True,value_list=insert_vals)
                cur_user = Admin(sql.select(self.cursor,['*'],self.userTable,f"ID = '{ID}'",print=0))
                self.Aseed = ID
            else:
                sql.insert(self.cursor,self.userTable,single_value=True,value_list=insert_vals)
                cur_user = User(sql.select(self.cursor,['*'],self.userTable,f"ID = '{ID}'",print=0))
                self.Useed = ID
            print("Sign Up Process complete!")
            return cur_user


    def searchBooks(self):
        attribute_db = ['ID','name','author','ISBN','publication','genre','times_borrowed','unavailable']
        prompts = {
            1 : "\n".join([str(x)+' for '+ attribute_db[x] for x in range(len(attribute_db))]),
            3 : "Enter the parameter number in a list with the first parameter chosen going first: ",
            4 : "Enter the subcategory/ies in the form of a list: ",
            5 : "Enter BookIDS of books you wish to use later if none enter -1",
            6 : "Looks like the book is unavailable: "
        }
        print(prompts[1])
        param_selected = int(eval(input(prompts[3]))[0])
        if(param_selected in range(len(attribute_db))):
            if(param_selected not in [0,1,3]):
                sql.select(self.cursor,[f'DISTINCT {param_selected}'])
                subcats = eval(input(prompts[4]))
                for subcat in subcats:
                    sql.select(self.cursor,['*'],self.booksTable,[f"{attribute_db[param_selected]} = '{subcat}'"],['times_borrowed'],True)
            else:
                approx_string = input("Enter a keyword/ID/ISBN: ")
                result = sql.select(self.cursor,['*'],self.booksTable,[f'{attribute_db[param_selected]} LIKE "%{approx_string}%"'],print=0)
                if(not result):
                    print(prompts[6])
                    return
                else:
                    print(result)
            books_selected = eval(input(prompts[5]))
            if(books_selected[0] == "-1"):
                return
            else:
                books_selected = [f"'{x.upper()}'" for x in books_selected]
                sql.select(self.cursor,['*'],self.booksTable,[f'{attribute_db[param_selected]} IN ({books_selected})'])
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
            'Number of Employees' : int(self.Aseed[5:])
        };
        for key,val in genInfo.items():
            print(f'{key} : {val}')
    

    def export_to_csv():
        pass

    def main_loop(self):
        pass