'''
Format of output:

n m
cap1 f1
cap2 f2
...
capn fn
d1 c11 c21 ... cn1
d2 c12 c22 ... cn2
...
dm c1m c2m ... cnm
'''

import random as rd

# n is the number of facilities
# m is the number os clients
n = rd.randint(3, 7)
m = rd.randint(3, 7)

sumOfCap = 0
sumOfD = 0

# cap[i] is the capacity of facility i
# f[i] is the cost to create/activate the facility i
# d[j] is the demand of the client j
# c[i][j] is the cost/profit to assign client j to facility i 
cap = [0 for i in range(n + 1)]
f = [0 for i in range(n + 1)]
d = [0 for j in range(m + 1)]
c = [[0 for j in range(m + 1)] for i in range(n + 1)]

# Creating cap and f
for i in range(1, n + 1):
    cap[i] = rd.randint(1, 100)
    f[i] = rd.randint(1, 100)
    sumOfCap += cap[i]

# Creating d and c
for j in range(1, m + 1):
    lim = min(100, sumOfCap - sumOfD)
    d[j] = rd.randint(0, lim)
    sumOfD += d[j]
    for i in range(1, n + 1):
        c[i][j] = rd.randint(1, 100)
        
print(f'{n} {m}')
for i in range(1, n + 1):
    print(f'{cap[i]} {f[i]}')
for j in range(1, m + 1):
    print(f'{d[j]} ', end='')
    for i in range(1, n + 1):
        print(f'{c[i][j]} ', end='')
    print()