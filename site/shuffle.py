import db
import logger

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
log = logger.Log('shuffle', 'logFile.log').get_logger()

db = db.DatabaseManager()
roles = db.getRuoli()
people = db.getPersone()

pairToRole = [-1] * len(people)//2 if len(people)%2==0 else [-1] * (len(people)//2+1)

for i in range(0, len(roles)):
    pairToRole[-i-1]=roles[i]['id']

#print(pairToRole)

mat = []
p = len(people)
if(p%2!=0):
    p+=1
'''
start = 0
if len(people)%2!=0:
    start = 1

t=[-1]*(p//2)
for i in range(start, p//2):
    t[i] = people[i-start]['id']
mat.append(t)

t=[]
for i in range(p//2, p):
    t.append(people[i-start]['id'])
mat.append(t)
pr(mat)
'''

mat=[[-1]*(p//2), [-1]*(p//2)]
for i in range(len(people)):
    if(i%2==0):
        mat[1][-(i//2)-1]=people[i]['id']
    else:
        mat[0][-(i//2)-1]=people[i]['id']
#print("now")
pr(mat)


ruota(mat)
log.info("first rotation")
ruota(mat)
log.info("second rotation")
pr(mat)
pair = getCoppie(mat)


#print(pair)
#print(pairToRole)

for i in range(1, len(pair)):
    db.updateRole(pair[i][0], pairToRole[i] if pairToRole[i]!=-1 else None)
    log.info("update %s --> " % (pair[i][0]) + str(pairToRole[i] if pairToRole[i]!=-1 else None))
    #print("update %s --> " % (pair[i][0]) , pairToRole[i] if pairToRole[i]!=-1 else None)
    db.updateRole(pair[i][1], pairToRole[i] if pairToRole[i]!=-1 else None)
    log.info("update %s --> " % (pair[i][0]) + str(pairToRole[i] if pairToRole[i]!=-1 else None))
    #print("update %s --> " % (pair[i][1]), pairToRole[i] if pairToRole[i]!=-1 else None)
db.close()