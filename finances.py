import pandas as pd
import numpy as np

class UFinances:
    
    def __init__(self,membership_fees,due_date):
        self.due_date = due_date
        self.membership_fees = membership_fees
        self.lost_books = pd.series()
        self.misc = pd.Series()
        self.TotalDue = 0
    
    def clear_all_dues(self):
        self.lost_books = pd.Series()
        self.misc = pd.Series()
        self.TotalDue = 0
    
    def pay_mem_fees(self):
        self.due_date = np.datetime64(self.due_date) + np.timedelta64(1,'M')
        self.TotalDue -= self.membership_fees
    
    def pay_lost_books(self):
        total_paid = sum(self.lost_books)
        self.TotalDue -= total_paid
    
    def pay_misc(self):
        total_paid = sum(self.misc)
        self.TotalDue -= total_paid
    
    
    
