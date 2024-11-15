def pr(mat):
    print("-"*6*len(mat[0]))
    for i in range(len(mat[0])):
        print("%5s" % mat[0][i], end=" ")
    print()
    for i in range(len(mat[1])):
        print("%5s" % mat[1][i], end=" ")
    print()
    print("-"*6*len(mat[0]))
    print("\n")
    
    
def getCoppie(mat):
    pr(mat)
    '''for i in range(0, len(mat[0])):
        print(mat[0][i], " --> ", mat[1][i])
    print()'''

def ruota(mat):
    last = mat[0][-1]
    for i in range(len(mat[0])-1, 1, -1):
        mat[0][i]=mat[0][i-1]
        
    first = mat[1][0]
    for i in range(0, len(mat[1])-1):
        mat[1][i]=mat[1][i+1]
        
    mat[1][-1]=last
    mat[0][1]=first



mat = []
p = 15
if(p%2!=0):
    p+=1

t = []
for i in range(1, p//2+1):
      t.append(i)
mat.append(t)

t = []
for i in range(1, p//2+1):
      t.append(i+p//2)
mat.append(t)  

pr(mat)


for i in range(1, p-1):
    ruota(mat)
    getCoppie(mat)
        


