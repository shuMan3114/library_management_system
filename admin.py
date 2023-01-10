# from .modules.mailing import send_mail,format_mail
from passlib.hash import bcrypt
import getpass
from modules.options import optionValidator,pass_input
import graphing as graph
import sql_functions as sql

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


    def edit_books(self,BookID):
        prompts = {
            1 : "Enter 1 to change quantity 2 to change price 3 to drop book from database: ",
            2 : "Enter new value: ",
            3 : "Successfully updated new value!",
            4 : "Successfully dropped book!"
        }
        b_attr = {
            1 : 'quantity',
            2 : 'price'
        }
        choice = optionValidator(prompts[1],lower_limit=1,higher_limit=3)
        if(choice == 0):
            return
        if(choice == 3):
            sql.delete(self.cursor,self.booksTable,f'bookID = "{BookID}"')
            print(prompts[4])
            return
        new_val = int(input(prompts[2]))
        sql.update(self.cursor,self.booksTable,[b_attr[choice]],[new_val],f'bookID= "{BookID}"')
        print(prompts[3])

    def delete_user_account(self,userID):
        sql.delete(self.cursor,self.userTable,f'userID = "{userID}"')
        

    def graphing(self):
        prompts = {
            1 : "Enter 1 to plot Book based graphs 2 to plot user based graphs and 3 to exit: ",
            2 : "Enter 1 to plot max() 2 to plot min() 3 to plot total 4 to plot count() based graphs: ",
            3 : "Enter 1 to plot wrt to publication 2 to plot wrt to author 3 to plot wrt to genre: ",
            4 : "Enter 1 to plot histogram of count of borrowed_lists 2 to plot histogram of count of wish_list: "
        }
        agg_mode_dict= {
            1 : 'max',
            2 : 'min',
            3 : 'sum',
            4 : 'count'
        }
        attribute_dict = {
            1 : 'publication',
            2 : 'author',
            3 : 'genre',
            4 : 'count_borrowed_list',
            5 : 'count_wish_list'
        }
        choice = optionValidator(prompts[1],lower_limit=1,higher_limit=3)
        if(choice in [3,0]):
            return
        if(choice == 1):
            aggregate_mode = optionValidator(prompts[2],lower_limit=1,higher_limit=4)
            if(aggregate_mode ==0):
                self.graphing()
                return
            attr_chosen = optionValidator(prompts[3],lower_limit=1,higher_limit=3)
            if(attr_chosen == 0):
                self.graphing()
                return
            aggregate = agg_mode_dict[aggregate_mode]
            attribute = attribute_dict[attr_chosen]
            graph.BookVAttr(self.cursor,self.booksTable,attribute,aggregate)
        else:
            attr_chosen = optionValidator(prompts[4],lower_limit=1,higher_limit=2)
            if(attr_chosen == 0):
                self.graphing()
                return
            attr = attribute_dict[attr_chosen + 3]
            graph.UserStats(self.cursor,self.userTable,attr)

            