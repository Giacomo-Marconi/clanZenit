def getCoppie(n, time, role):
    
    check = []
    for x in range(n):
        a=[]
        for y in range(n):
            a.append(False)
        check.append(a)
    
    i=0
    check[i][i] = True
    c=0
    r=0
    while(r<n):
        print("------------------------------")
        for x in range(n):
            print(check[x])
        if(check[r][r]):
            r+=1
            c=r
            print("skippato --> ", r-1)
            continue
                
        print("cerco in: ", r)
        while(check[r][c] or c==r):
            find = False
                
            print(c, end=" ")
            c+=1
                
        check[r][c] = True
        check[c][r] = True
        print(f"\n find: {r} --> {c}")
        r+=1
        c=r
        
            
    


def shift(array, n):    
    return array[n:] + array[:n]

def coppie(pers, diff, time):
    array = shift(pers, time)
    print("[", end="")
    used = [0] * len(array)
    sel = -1
    done = 0;
    while done < len(role):
        sel += 1
        if(used[sel] == 1):
            continue
        used[sel] = 1
        used[(sel+diff)%len(array)] = 1
        print(f" {array[sel]} --> {array[(sel+diff)%len(array)]}  ", end="")
        done += 1
    #tostaaaisssima pazzo cane cane pazzo
    
    print("]", end=" no used: ")
    
    for i in range(len(used)):
        if(used[i] == 0):
            print(array[i], "", end=" ")
            
    print()
        

p = 12
r = 5

person = []
for i in range(p):
    person.append(i+1)
#print(person)

role = []
for i in range(r):
    role.append(chr(i+97))
#print(role)

"""
while True:
    input("next rotation: ")
    person = shift(person, 2)
    if(person[0] == 1):
        person = shift(person, 1)
    print(person)
    print(role)

time = 1
diff = 0
while True:
    input("next rotation: ")
    diff+=1
    if(diff == len(person)):
        diff = 1
    
    coppie(person, diff, time)
    time += 1
    if(time == len(person)):
        time = 1
    print(role)
"""
    
    
    
#1 --> 23 45 67 --> 1
#2 --> 13 46 57 --> 2
#3 --> 12 47 56 --> 3
#4 --> 15 26 37 --> 4
#5 --> 14 27 36 --> 5
#6 --> 17 24 35 --> 6
#7 --> 16 25 34 --> 7


time = 0
p = 7
r = 3
while True:
    input("next rotation: ")
    time += 1
    if(time == p):
        break

    getCoppie(p, time, r)
    