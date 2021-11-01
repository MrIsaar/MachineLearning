import math
def cost (y,w,x,b):
    if(len(y) != len(x)):
        raise Exception()
    sum = 0
    for i in range(0,len(y)):
        suminner = 0
        if(len(x[i]) != len(w)):
                raise Exception()
        for j in range (0,len(w)):
            suminner += (x[i][j] * w[j])
        suminner = (y[i] - suminner)**2
        sum += suminner
    sum = sum/2
    return sum + b/2

def generate():
    s = [-1,1]
    r = []
    for x1 in range(2):
        for y2 in range(2):
            for z3 in range(2):
                for a4 in range(2):
                    for b5 in range(2):
                        for c6 in range(2):
                            for d7 in range(2):
                                for e8 in range(2):
                                    for f9 in range(2):
                                        for g10 in range(2):
                                            for h11 in range(2):
                                                r.append([s[x1],s[y2],s[z3],s[a4],s[b5],s[c6],s[d7],s[e8],s[f9],s[g10],s[h11] ])
    return r


def distfromline(line,bias,point,normalize=1):
    if len(line) != len(point):
        raise Exception("not same dimentions")
    output = "| bias"
    denom = 0
    sum = 0
    mag = 0
    for i in range(len(line)):
        mag += line[i]**2
        if line[i] != 0:
            denom += 1
        sum += (line[i]/normalize)*point[i]
        sign = "+"
        if line[i] < 0:
            sign = "-"
        if line[i] != 0:
            output += sign + "x_"+str(i+1)
    sum = float(abs(sum+bias))
    mag = math.sqrt(mag)
    #print(output+" |")
    #print("\\sqrt(" + str(denom) + ")")
    return sum/mag

line = [-1,-1,-1,-1,1,1,1,1,0,0,0]
bias = -1
point = [[ 1**(i-1) for i in range(len(line))]]

line = [83,-68]
bias = 3876
point = [[98,15],[20,81],[30,98]]

#point = (generate())
mi = 100
for i in range(len(point)):
    c = distfromline(line,bias,point[i])
    mi = min(mi,c)
    print("point[",i,"] = ",point[i]," : ",c)
print (mi)

