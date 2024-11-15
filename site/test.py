mat = []
p = 7
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

def pr(mar):
    print(mat[0])
    print(mat[1])
    print()

pr(mat)
    
def ruota(mat):
    last = mat[0][-1]
    for i in range(len(mat[0])-1, 1, -1):
        mat[0][i]=mat[0][i-1]
        
    first = mat[1][0]
    for i in range(0, len(mat[1])-1):
        mat[1][i]=mat[1][i+1]
        
    mat[1][-1]=last
    mat[0][1]=first
    pr(mat)
    



for i in range(1, p-1):
    ruota(mat)
    
        
        
        


