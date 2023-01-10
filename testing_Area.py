import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
import bcrypt

df = pd.DataFrame(np.reshape(np.arange(12), (3,4)) , columns= ['0','1','2','3'])

query_str = ""
for row,row_series in df.iterrows():
    query_str += f'({",".join([str(x) for x in list(row_series.values)])}),'

query_str = query_str[:-1] + ";"
print(query_str)


