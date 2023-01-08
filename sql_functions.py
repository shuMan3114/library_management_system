# Querying the database and then making that an object for manipulation
# Updating database once query is done
# Extracting specific data.
# Most borrowed book etc.

import pandas as pd
import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
        'Server=RON\SQLEXPRESS;'
        'Database=test_database;'
        'Trusted_Connection=yes;')

def select(cursor,display_fields,tname,condition = None,group_by=None,having=None,order_by=None,desc=None,print=1):
    if(display_fields[0] == '*'):
        fields = "*"
    else:
        fields = ",".join(display_fields)
    
    if(condition == None):
        query_str = f'SELECT {fields} FROM {tname} '
    else:
        query_str = f'SELECT {fields} FROM {tname} WHERE {condition} '
    
    if(group_by != None):
        query_str += f'GROUP BY {group_by} '
    if(having != None):
        query_str += f'HAVING {having} '
    
    if(desc == True):
        query_str += f'ORDER BY {order_by} DESC;'
    elif(desc == False):
        query_str += f'ORDER BY {order_by} ASC;'
    else:
        query_str += ';'
    out_df = pd.read_sql_query(query_str,cursor)
    if(print):
        print(out_df)
    else:
        return out_df


def update(cursor,t_name,updation_fields,new_values,condition):
    for i in range(len(updation_fields)):
        query_str = f'UPDATE {t_name} SET {updation_fields[i]} = {new_values[i]} WHERE {condition}'
        cursor.execute(query_str)
        print("Updated Record",select(cursor,['*'],t_name,condition),sep="\n")


def insert(cursor,t_name,values,record_df,value_list=None,single_value=False):
    if(values):
        query_str = f'INSERT INTO {t_name} ({",".join(values)}) VALUES'
    else:
        query_str = f'INSERT INTO {t_name} VALUES'
    if(not single_value):
        for row,row_series in record_df.iterrows():
            query_str += f'({",".join([str(x) for x in list(row_series.values)])}),'
        query_str = query_str[:-1] + ";"
    else:
        query_str += f'({",".join([str(x) for x in single_value])}'
    cursor.execute(query_str)


def delete(cursor,t_name,condition):
    query_str = f'DELETE FROM {t_name} WHERE {condition};'
    cursor.execute(query_str)

