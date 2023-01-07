'''
structure :
books -- name , author , ISBN , type , times_borrowed , borrowed
user -- userID , first name , last name , email, phone , membership_level , payment_due
fines_db -- userID , total_fine , fines_paid, fine_due
borrowed - ISBN, userID , date_borrowed , date_returned(predictive)

'''

class Book:

    def __init__(self,bookID,b_name,author,publication,ISBN,genre,price,quantity):
        self.BookID = bookID
        self.name = b_name
        self.author = author
        self.ISBN = ISBN
        self.publication = publication
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.books_borrowed = 0
        self.times_borrowed = 0
        self.unavailable = False
    
    def update_quantity(self,new_quantity):
        self.quantity += new_quantity
        

    def update_borrowed_book_status(self,UserID):
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