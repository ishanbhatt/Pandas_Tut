import numpy as np
Array = np.array([[1,2,3], [4,5,6], [7,8,9], [15,11,13], [18,14,20] ]) 
(rows,cols)=Array.shape
for i in xrange(rows):
    if Array[i][0] > Array[i][1]:
        print i
        break