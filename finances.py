import pandas as pd

class UFinances:
    
    def __init__(self,membership_fees,due_date):
        self.due_date = due_date
        self.membership_fees = membership_fees
        self.lost_books = pd.series()
        self.misc = pd.Series()
        self.TotalDue = self.membership_fees
    
    
    
