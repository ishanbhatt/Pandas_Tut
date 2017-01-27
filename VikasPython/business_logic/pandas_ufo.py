'''
Created on Nov 4, 2016

@author: Ishan.Bhatt
Here we will explore loc, iloc, ix
'''
import pandas as pd

ufo = pd.read_csv('http://bit.ly/uforeports',nrows=10)

# print ufo.loc[0, :] #0 - 0th row , : all columns
# print ufo.loc[[0,1,2] , :] #3 rows all columns
# print ufo.loc[0:2 , :] SAME AS ABOVE inclusive on both sides unlike range
print '-'*100

df1 = ufo.loc[:, ['City','State']] #You can use loc to get colums and put it in another df
# df1['combined'] = "{},{}".format(df1['City'],df1['State'])
print 'AAAAAAAAAAAAAAAAAAAAAAAAA'
l = [0,1]
df1['combined'] = df1[l].apply(','.join, axis=1)
# print df1.iloc[:,(0,1)]
print df1

print '-'*100
#Let's do conditions in loc

# print ufo.loc[ufo.City=='Oakland','State'] #Select all states(column) with city==Oakland
#iloc just works like loc. but as range exclusive-inclusive

# print '-'*100
# print ufo.iloc[:, 0:4]#Gives columns 0,1,2,3

