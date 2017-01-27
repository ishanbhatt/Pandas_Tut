'''
Created on Nov 2, 2016

@author: Ishan.Bhatt
'''
import csv
import time

start_time = time.time()
reader1 = csv.reader(open(r"D:\\VikasStuff\\FL_insurance_first.csv"))
reader2 = csv.reader(open(r"D:\\VikasStuff\\FL_insurance_second.csv"))

count = 0
same_count = 0
li = []

for _ in reader1:
    same_count += 1
    for _ in reader2:
        count += 1



print "Total records read " + str(count)
print "Total records same " + str(same_count)

another_count = 0
for i in xrange(0,600000):
    for j in xrange(0,600000):
        pass

print another_count
end_time = time.time()
print "Total time taken :" + str(end_time - start_time)

