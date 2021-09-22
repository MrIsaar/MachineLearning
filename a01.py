import math

def entropy(_pos,_total):
    plus=_pos/_total
    minus=(_total-_pos)/_total
    
    #print("p+: " + str(-(plus*math.log(plus,2))) + ", p-: " + str((-minus*math.log(minus,2))) )
    if(plus == 0):
        return (minus*math.log(minus,2))
    if(minus == 0):
        return (plus*math.log(plus,2))
    return -(plus*math.log(plus,2)) - (minus*math.log(minus,2))
def giniIndex(pos,total):
    if total == 0:
        return 0
    neg = total - pos
    return 1 - ((pos/total)**2 + (neg/total)**2)



total = 14

#entropy
pos = 2
neg = total - pos
posp = 2
negp = 0
e1= entropy(posp,pos)
e2= entropy(negp,neg)
e = e1 * (pos/total) + e2 * (neg/total)
#print(str(e1) + "(" + str(pos)+"/" + str(total) + ") + " + str(e2) + "(" + str(neg)+"/" + str(total) + ") = " + str(e))

#giniIndex
sum = 5
origin = giniIndex(2,sum)
pos   = [3,2,0]
total = [3,2,0]
g = [0,0,0]
g[0] = giniIndex(pos[0],total[0])
g[1] = giniIndex(pos[1],total[1])
g[2] = giniIndex(pos[2],total[2])
EGI = (total[0]/sum)*g[0] + (total[1]/sum)*g[1] + (total[2]/sum)*g[2]
print ("EGI= " + str(EGI))
print ("gain= " + str(origin - EGI))

