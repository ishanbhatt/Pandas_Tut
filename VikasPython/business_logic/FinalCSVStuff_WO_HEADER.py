'''
Created on Nov 7, 2016

@author: Ishan.Bhatt
'''
import csv
import sys
import argparse
import pandas as pd
#from _regex_core import String
from __builtin__ import str
import os
import pdb
from pandas.io.tests.parser import skiprows
import time


def read_key_rules(keys_path):
    key_rules = {}
    with open(keys_path, 'r') as csvfile:
        key_reader = csv.reader(csvfile, delimiter = ':')
        for row in key_reader:
            key_rules[row[0]] = row[1].split(',')
    return key_rules

def get_keys(file1, key_rules):
    for fname,keys in key_rules.iteritems():
        if fname in file1:
            return keys #It's a char list like ['0','1','2']

def get_non_keys(file1,keys):
    
    file1_read=pd.read_csv(file1,nrows=2,sep=',|\|',engine='python') 
    (_,cols) = file1_read.shape 
    all_keys = set(range(cols - 1))# To ignore timestamp_col & last column as  non key part
    timestamp_col_index = cols - 2 # save index of timestamp column
    all_keys.remove(timestamp_col_index)
    keys = map(int, keys)
    keys=set(keys)
    non_keys = all_keys - keys
    return (list(non_keys), timestamp_col_index,list(all_keys))

def compare_csv(file1, file2, keys, non_keys, timestamp_col_index,all_keys, op_folder):
    '''
    Here we will have comparison logic to create 5 different files in op_folder.
    Get the key columns' data from both csv and make crc and compare them.
    Now we are getting 0,1 keys for UBSRTOUBSR_ACCTPGP file.
    df1 - Vision
    df2 - UBSR
    df3 - Matched with keys only data.
    '''
    df1 = pd.read_csv(file1,header=None,sep=',|\|',engine='python')
    df2 = pd.read_csv(file2,header=None,sep=',|\|',engine='python')

    
    keys = map(int, keys)
    df1=df1.applymap(str)
    df2=df2.applymap(str)
    
    df1['crc'] = df1[keys].apply(','.join, axis=1)
    df2['crc'] = df2[keys].apply(','.join, axis=1)
    
    df2.set_index('crc', inplace = True)
 
    perfectly_matched_file = os.path.join(op_folder,'perfect_matched.csv')
    partially_matched_file = os.path.join(op_folder,'partial_matched.csv')
    ubsr_updated = os.path.join(op_folder,'ubsr_updated.csv')
    vision_only_file = os.path.join(op_folder,'vision_only.csv')
    ubsr_only_file = os.path.join(op_folder,'ubsr_only.csv')
    
    
    df3 = df1.loc[df1.crc.isin(df2.index)].drop('crc', axis=1)#partial vision data including timestamp from vision
    df2.reset_index(drop=True, inplace=True)
    df1.set_index('crc', inplace = True)
    df2['crc'] = df2[keys].apply(','.join, axis=1)
    df4 = df2.loc[df2.crc.isin(df1.index)].drop('crc', axis=1) #partial ubsr data including timestamp from ubsr
    df2.set_index('crc', inplace = True)
    df1.reset_index(drop=True, inplace=True)
    df1['crc'] = df1[keys].apply(','.join, axis=1)
    df1.loc[~df1.crc.isin(df2.index)].drop('crc', axis=1).to_csv(vision_only_file, index=False, header = False)
    #Changing string timestamp into datetime object
    df3.iloc[:,timestamp_col_index] = pd.to_datetime(df3.iloc[:,timestamp_col_index],format='%Y-%m-%d-%H.%M.%S')
    df4.iloc[:,timestamp_col_index] = pd.to_datetime(df4.iloc[:,timestamp_col_index],format='%Y-%m-%d-%H.%M.%S')
    
    
   
    df5 = pd.concat([df3,df4]).sort_values(timestamp_col_index,ascending=False)
    df5.reset_index(drop=True, inplace=True)
    df5.drop_duplicates(all_keys,keep=False,inplace=True)
    
    #df6 will have latest timestamp file of partially matched file
    df6=df5.sort_values([timestamp_col_index],ascending=False).drop_duplicates(keys,keep='first')
    df1['all_keys'] = df1[all_keys].apply(','.join, axis=1)
    df1.set_index('all_keys', inplace = True)
    df6['all_keys']=df6[all_keys].apply(','.join, axis=1)
    
    
    df6.loc[df6.all_keys.isin(df1.index)].drop('all_keys',axis=1).to_csv(partially_matched_file, index=False, header = False)
    df2['all_keys'] = df2[all_keys].apply(','.join, axis=1)
    df2.set_index('all_keys', inplace = True)
    df6.loc[df6.all_keys.isin(df2.index)].drop('all_keys',axis=1).to_csv(ubsr_updated, index=False, header = False)
    df2['crc'] = df2[keys].apply(','.join, axis=1)
    df2.set_index('crc', inplace = True)
    
    df3['non_key'] = df3[non_keys].apply(','.join, axis=1)
    
    df2.rename_axis(None)
    df2['non_key'] = df2[non_keys].apply(','.join, axis=1)
    df2.set_index('non_key', inplace=True)
    
    df4['non_key']=df4[non_keys].apply(','.join, axis=1)
    df4.set_index('non_key', inplace = True)
    df3.loc[df3.non_key.isin(df4.index)].drop('non_key', axis=1).to_csv(perfectly_matched_file, index=False, header = False)
    #####df3.loc[~df3.non_key.isin(df2.index)].drop('non_key', axis=1).to_csv(partially_matched_file, index=False, header = False)
    
    
    
    df2['crc'] = df2[keys].apply(','.join, axis=1)
    df2.reset_index(drop=True, inplace=True)
    df1.set_index('crc',inplace =True)
    
    df2.loc[~df2.crc.isin(df1.index)].drop('crc', axis=1).to_csv(ubsr_only_file, index=False, header=False)
    
def main(arguments):
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', action='store', dest='keys_file', help='Path of keys file', required=True)
    parser.add_argument('-f', action='store', dest='first_csv', help='Path of first csv file', required=True)
    parser.add_argument('-s', action='store', dest='second_csv', help='Path of second csv file', required=True)
    parser.add_argument('-o', action='store', dest='op_folder', help='Path of keys file', required=True)
    
    args = parser.parse_args(arguments)
    
    key_rules = read_key_rules(args.keys_file)
    keys = get_keys(args.first_csv, key_rules)
    (non_keys ,timestamp_col_index,all_keys) = get_non_keys(args.first_csv, keys) 
    if keys:
        compare_csv(args.first_csv, args.second_csv, keys, non_keys, timestamp_col_index,all_keys ,args.op_folder)
    else:
        raise "File format not correct"
    end_time = time.time()
    print end_time-start_time
if __name__ == '__main__':
    main(sys.argv[1:])