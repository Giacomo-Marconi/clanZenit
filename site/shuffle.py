import db

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
    pairs = []
    for i in range(0, len(mat[0])):
        pairs.append([mat[0][i], mat[1][i]])
    return pairs

def ruota(mat):
    last = mat[0][-1]
    for i in range(len(mat[0])-1, 1, -1):
        mat[0][i]=mat[0][i-1]
        
    first = mat[1][0]
    for i in range(0, len(mat[1])-1):
        mat[1][i]=mat[1][i+1]
        
    mat[1][-1]=last
    mat[0][1]=first


db = db.DatabaseManager()
roles = db.getRuoli()
people = db.getPersone()

pairToRole = [-1] * len(people)

for i in range(0, len(roles)):
    pairToRole[-i-1]=roles[i]['id']

print(pairToRole)

mat = []
p = len(people)
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

ruota(mat)
pr(mat)
pair = getCoppie(mat)

    
print(pair)
print(pairToRole)

