import sys
from collections import Counter

cnt_open = Counter()
cnt_login = Counter()

access = []

print(sys.argv[1])

with open(sys.argv[1], 'r') as f:
    access1 = f.readlines()
    for line in access1:
        access.append(line.split(" - "))
    
    for log in access:
        cnt_open[log[0]] += 1
        if log[1][0:5] == "rinri":
            cnt_login[log[0]] += 1
       
    print("all")
    print(cnt_open)
    print("login")
    print(cnt_login)
