import time
start_time = time.time()
import pandas as pd
from pandas import DataFrame
import datetime
import pandas_datareader.data as web
import numpy as np 
from pandas.util.testing import assert_frame_equal
import pdb


#sp500 = web.DataReader("GOOGL", 'yahoo', start=datetime.datetime(2006, 10, 1), end=datetime.datetime(2016, 1, 1))
#sp500.to_csv(r'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\huge_csv\sample.csv')




# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# We want to be able to easily tell which rows have changes
def has_change(row):
    if "--->" in row.to_string():
		return "Y"
    else:
        return "N"

# Read in both excel files
df1 = pd.read_csv(r'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\huge_csv\FL_insurance_first.csv',header=None)#,index_col='policyID', parse_dates=True)
#df2 = pd.read_csv(r'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\huge_csv\FL_insurance_second.csv')#,nrows=10000)#,index_col='policyID', parse_dates=True)

# for index, row in df1.iterrows():
    # print row, index
# (rows,cols) = df1.shape
# for i in xrange(rows):
    # print df1.loc[i+1]
print str(df1) +"Ashish"
end_time = time.time()
print "Total time taken :" + str(end_time - start_time)
# # Make sure we order by account number so the comparisons work
df1.sort(columns="policyID")
df1=df1.reindex()
df2.sort(columns="policyID")
df2=df2.reindex()


# # Create a panel of the two dataframes
diff_panel = pd.Panel(dict(df1=df1,df2=df2))

# #Apply the diff function
diff_output = diff_panel.apply(report_diff, axis=0)

diff_output.to_csv(r'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\huge_csv\my-diff-1.csv',index=False)

# # Flag all the changes
#diff_output['has_change'] = diff_output.apply(has_change, axis=1)

# #Save the changes to excel but only include the columns we care about
#diff_output[(diff_output.has_change == 'Y')].to_csv(r'C:\Users\Ashish.Bainade@infovisionlabs.com\Desktop\huge_csv\my-diff-1.csv',index=False)#,columns=["account number","name","street","city","state","postal code"])






