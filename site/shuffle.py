import db as dbm
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
    mat2 = mat.copy()
    mat2[0]=[mat[0][0]] + [mat[1][0]] + mat[0][1:]
    mat2[1]=mat[1] + [mat[0][len(mat[0])-1]]
    
    #print(mat2)
    
    mat[0]=mat2[0][:-1]
    mat[1]=mat2[1][1:]
    
log = logger.Log('shuffle', 'logFile.log').get_logger()



def shuffle():
    try:
        db = dbm.DatabaseManager()
        roles = db.getRuoli()
        people = db.getPersone()

        pairToRole = [-1] * ((len(people)//2) if len(people)%2==0 else [-1] * (len(people)//2+1))

        for i in range(0, len(roles)):
            pairToRole[-i-1]=roles[i]['id']

        #print(pairToRole)

        mat = []
        p = len(people)
        if(p%2!=0):
            p+=1
            
        print(people)
        print(pairToRole)
        

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

        for i in range(0, len(pair)):
            db.updateRole(pair[i][0], pairToRole[i] if pairToRole[i]!=-1 else None)
            log.info("update %s --> " % (pair[i][0]) + str(pairToRole[i] if pairToRole[i]!=-1 else None))
            db.updateRole(pair[i][1], pairToRole[i] if pairToRole[i]!=-1 else None)
            log.info("update %s --> " % (pair[i][1]) + str(pairToRole[i] if pairToRole[i]!=-1 else None))
        db.close()
        return True
    except Exception as e:
        print(e)
        return False



def shuffle2():
    try:
        db = dbm.DatabaseManager()
        roles = db.getRuoli()
        people = db.getPersone()

        # Inizializza pairToRole in base al numero di coppie
        num_pairs = (len(people) + 1) // 2  # Gestisce sia pari che dispari
        pairToRole = [-1] * num_pairs

        # Assegna i ruoli alle coppie (partendo dalla fine)
        for i in range(min(len(roles), num_pairs)):
            pairToRole[-(i + 1)] = roles[i]['id']

        # Crea la matrice per le coppie
        mat = [[-1] * num_pairs, [-1] * num_pairs]
        for i in range(len(people)):
            if i % 2 == 0:
                mat[0][-(i // 2) - 1] = people[i]['id']  # Seconda riga (indici pari)
            else:
                mat[1][-(i // 2) - 1] = people[i]['id']  # Prima riga (indici dispari)

        # Ruota la matrice due volte
        pr(mat)
        ruota(mat)  # Prima rotazione
        ruota(mat)  # Seconda rotazione
        pr(mat)
        # Estrae le coppie dalla matrice ruotata
        pairs = getCoppie(mat)

        # Assegna i ruoli alle coppie
        for i in range(len(pairs)):
            role_id = pairToRole[i] if pairToRole[i] != -1 else None
            db.updateRole(pairs[i][0], role_id)
            db.updateRole(pairs[i][1], role_id)
            log.info(f"Updated {pairs[i][0]} and {pairs[i][1]} --> {role_id}")

        db.close()
        return True
    except Exception as e:
        log.error(f"Error in shuffle: {e}")
        return False


if(__name__ == "__main__"):
    if(shuffle2()):
        print("done")