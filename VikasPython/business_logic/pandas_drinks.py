'''
Created on Nov 4, 2016

@author: Ishan.Bhatt
'''
import pandas as pd

drinks = pd.read_csv('http://bit.ly/drinksbycountry')

drinks.set_index('country', inplace = True)
print drinks.head()

print '-'*100
print drinks.index
''' As you can see in the following two lines, index is not a part of dataframe.
    Always select something meaningful as index, As loc is faster lookup.
    To fetch any particular column, do drinks.beer_serving
'''
print drinks.columns
print drinks.shape

print '- ALBANIA BEER'*100
print drinks.loc['Albania']
print drinks.continent #As you can see it comes with the index country.

print '-'*100
print drinks.continent.value_counts() #This works as count(1) of sql query. It returns a series object.
print drinks.continent.value_counts()['Asia']
print drinks.continent.value_counts().values #Here you have only values not continent name. This is the series.
print drinks.continent.value_counts().sort_values() #It is sorted by values 12,16 ..., how to do with index?
print drinks.continent.value_counts().sort_index()

#Experiments with ix
#like loc and iloc but it can handle both integer index as well as Keys
print '-'*100
print drinks.ix['Albania':'Andorra', 0:2]
