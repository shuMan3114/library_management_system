import numpy as np
import getpass
from datetime import date
from passlib.hash import bcrypt
from .modules.mailing import send_mail,format_mail
from finances import UFinances


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

def print_dict(dict,filler = "-",headers = ["key","value"]):
    dict_keys = sorted([x for x in dict.keys()])
    final_output = " ".join([str(headers[0]), str(filler), str(headers[1])])
    for key in dict_keys:
        final_output += " ".join(["\n", str(key), str(filler), str(dict[key])])
    return final_output
    
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
        self.paymentDue = UFinances(membership_fees=self.monthlyFees,due_date=self.dueDate)



    def verify_login(self,entered_password):
        hasher = bcrypt.using(rounds=13)
        verdict = hasher.verify(entered_password, self.password)
        return verdict


    def forgot_password(self):
            code = 'alphanumeric_string'
            send_mail(self.contact,code)
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
            3: "Book(s) removed/added successfully!",
            4: "Waitlist cleared!",
            5: f"Sucssfully exited program! waitlist is: {self.waitlist}"
        }
        option_selected = option_validator(prompts[1],1,4)
        while(option_selected != 4):
            if(option_selected in [1,2]):
                print(self.waitlist)
                book_list = eval(input(prompts[2]))
                if(option_selected == 1):
                    self.waitlist = self.waitlist + book_list
                else:
                    self.waitlist = self.waitlist - book_list
                print(prompts[3])
            elif(option_selected == 3):
                self.waitlist = []
                print(prompts[4])
            
            option_selected = option_validator(prompts[1],1,4)
        
        return prompts[5]
    
    def make_payment(self):
        prompts = {
            1: "Enter 1 to pay all dues 2 to pay membership_fees 3 to pay lost_books 4 to pay misc prices 5 to pay part of the total due 6 to exit: ",
            2: "Enter amount to pay: ",
            3: "Successfully paid due!",
            4: f"Program exited successfully! Dues snapshot: {self.paymentDue.print_all()}"
        }
        print(f"BreakUp : \n{self.paymentDue.print_all()}")
        functionsDict = {
            1: self.paymentDue.clear_all_dues,
            2: self.paymentDue.pay_mem_fees,
            3: self.paymentDue.pay_lost_books,
            4: self.paymentDue.pay_misc
        }
        option_selected = option_validator(prompts[1],1,6)
        while option_selected != 5:
            functionsDict[option_selected]() #Might cause an error -- sort out in testing
            if(option_selected == 2):
                self.dueDate = np.datetime64(self.dueDate) + np.timedelta64(1,'M')
            print(prompts[3])
            option_selected = option_validator(prompts[1],1,6)
        return prompts[4]


    def update_mem_level(self):
        cur_memLevel = self.membership_level
        mem_l_dict ={
            0 : [0,1],
            1 : [20,3],
            2 : [40,5],
            3 : [60,7]
        }
        option_str = print_dict(mem_l_dict,filler="for",headers=["option",["fee","max_limit_to borrow"]])
        prompts = {
            1 : f"Current membership level: {cur_memLevel} -> monthly fees: {self.monthlyFees} -> borrow limit : {self.maxLimit}",
            2 : "Enter 1 to update membership status 2 to exit",
            3 : f"Enter\n{option_str}\n",
            4 : "Please pay all dues and the initial fee to update membership!",
            5 : "Enter 1 to clear all dues and pay initial fee 2 to pay only initial fee 3 to pay none 4 to exit procedure: ",
            6 : "Membership status updated successfully!",
            7 : "Program exited successfully!"
        }
        print(prompts[1])
        option_selected = option_validator(prompts[2],1,2)
        while option_selected !=2:
            new_mem_level = option_validator(prompts[3],0,3)
            if(self.paymentDue.TotalDue):
                print(prompts[4])
                payment_option = option_validator(prompts[5],1,4)
                if(payment_option == 1):
                    self.paymentDue.clear_all_dues()
                elif(payment_option == 3):
                    self.paymentDue.TotalDue += mem_l_dict[new_mem_level][0]
                elif(payment_option == 4):
                    break
            self.membership_level = new_mem_level
            self.monthlyFees = mem_l_dict[new_mem_level][0]
            self.maxLimit = mem_l_dict[new_mem_level][1]
            self.joinDate = date.today()
            if(new_mem_level):
                self.dueDate = np.datetime64(date.today()) + np.timedelta64(1,'M')
            self.paymentDue.due_date = self.dueDate
            self.paymentDue.membership_fees = self.monthlyFees
            
            print(prompts[6])
            option_selected = option_validator(prompts[2],1,2)
        return prompts[7]
        