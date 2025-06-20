import itertools as it
import numpy as np
import math

n = 6

s = list(range(1,n+1))
print(s)
permut = it.permutations(s)

with open("permutations.txt",'a') as f:
    f.write(str(math.factorial(n)))
    for j in permut:
        f.write('\n')
        for i in range(len(j)):
            f.write(str(j[i]) + " " ) 
