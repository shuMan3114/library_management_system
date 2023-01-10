'''
structure :
books -- name , author , ISBN , type , times_borrowed , borrowed
user -- userID , first name , last name , email, phone , membership_level , payment_due
fines_db -- userID , total_fine , fines_paid, fine_due
borrowed - ISBN, userID , date_borrowed , date_returned(predictive)

'''

class Book:

    def __init__(self,bookDf):
        self.BookID = bookDf['bookID']
        self.name = bookDf['name'] 
        self.author = bookDf['author'] 
        self.ISBN = bookDf['ISBN'] 
        self.publication = bookDf['publication']
        self.genre = bookDf['genre']
        self.price = bookDf['price']
        self.quantity = bookDf['quantity']
        self.books_borrowed = bookDf['books_borrowed']
        self.times_borrowed = bookDf['times_borrowed']
        self.unavailable = bookDf['unavailable'] 
    
    def update_quantity(self,new_quantity):
        self.quantity += new_quantity
        

    def update_borrowed_book_status(self):
        if(not self.unavailable):
            books_left = self.quantity - self.books_borrowed - 1
            if(books_left):
                self.unavailable = True
            self.books_borrowed += 1
            self.times_borrowed += 1
            return True
        else:
            return False
    

    def update_returned_book_status(self):
        self.books_borrowed -= 1
        if(self.unavailable):
            self.unavailable = False
        return "Book returned successfully!"