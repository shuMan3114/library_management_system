# Graphs borrowed books genre wise
# Total borrowed books per genre/publicaton/author
# Books per author/genre/publication
# User stattistics --> joindate and number of books borrowed
#  Most of these graphs will be frequency analysis graphs for users
# For books we have four variations :
# --> T.Quantity vs Author,Publication,Genre
# --> T.price vs Author,Publication,Genre
# --> Times_borrowed vs Author,Publication,Genre
# For Users we have:
# BorrowedList --> Bins analysis
# Dues --> Bins analysis

import pandas as pd
import matplotlib.pyplot as pl
import sql_functions as sql

# Book vs attribute graph:
def BookVAttr(cursor,t_name,attribute):
    book_attrs = ['quantity','timesBorrowed','price*quantity']
    # Price Graphs
    if(len(attribute) == 1):
        for b_attr in book_attrs:
            query_str = sql.select(cursor,[attribute,f'sum({b_attr})'],t_name,group_by={attribute})
            df = pd.read_sql_query(query_str,cursor)
            pl.bar(list(df[0]),df[1]) 
            pl.xlabel(attribute)
            pl.title(f'{attribute} vs {b_attr}')
            pl.show()
    else:
        for b_attr in book_attrs:
            query_str = sql.select(cursor,[b_attr],t_name,conditon=[f'{attribute[0]} = "{attribute[1]}"'])
            df = pd.read_sql_query(query_str,cursor)
            pl.hist(df[0],bins=40) 
            pl.xlabel(attribute[1])
            pl.title(f'{attribute[1]} vs {b_attr}')
            pl.show()


def UserStats(cursor,t_name,attribute):
    if(len(attribute) == 1):
        query_str = sql.select(cursor,[attribute],t_name)
        df = pd.read_sql_query(query_str,cursor)
        pl.hist(df[0],bins=40)
        pl.xlabel(attribute)
        pl.title(f'{attribute} vs number')
        pl.show()