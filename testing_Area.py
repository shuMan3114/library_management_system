import pandas as pd
import numpy as np

df = pd.DataFrame(np.reshape(np.arange(12), (3,4)) , columns= ['0','1','2','3'])

query_str = ""
for row,row_series in df.iterrows():
    query_str += f'({",".join([str(x) for x in list(row_series.values)])}),'

query_str = query_str[:-1] + ";"
print(query_str)

single_values = [1,"'2'","'3'",4,5]
print(",".join([str(x) for x in single_values]))

print(str(3*[0])+'1')


val = df['0'][0]
print(val)