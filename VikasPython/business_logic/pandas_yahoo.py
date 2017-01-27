'''
Created on Nov 3, 2016

@author: Ishan.Bhatt
'''
import pandas as pd
from pandas import DataFrame
import time

#Basically , we can use any operation and put it in pandas dataframe.
start_time = time.time()
df = pd.read_csv(r"D:\\VikasStuff\\FL_insurance_first.csv", index_col = 'policyID')
print df.head() #In print policyID shows below line, that specifies it's an index

df2 = df['tiv_2011'] #Getting only one column.
print '-' * 100
print df2.head()

df3 = df[['fr_site_limit','tiv_2011']] #I can use this to get key columns for the comparison.It works with integer columns index as well. in case you don't have column names.
print '-' * 100
print df3.head()
print '-' * 100
df4 = df3.rename(columns = {'tiv_2011' : 'TIV_2011'})
print df4.head()

#Some conditional stuff coming up.
print '-'*100
df5 = df3[(df3['tiv_2011'] > 1322376.0)]
print df5.head()
end_time = time.time()
print '-'*100


#SOme column based operations
df['1-2'] = df['point_granularity'] - df['fl_site_deductible']
print df.head()

df['difference'] = df['point_latitude'].diff()
print df['difference'].head()

print '-'*100
print df.describe()

#Mapping own functions on columns
print '-' * 100
def function(data):
    return data * 0

df['Zeroed_out'] = map(function, df['tiv_2011'])
print df.head()