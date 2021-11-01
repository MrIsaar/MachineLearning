import random
from perceptron import perceptron
def randomPoints(dim,points):
    val = [-1,1]
    p = []
    for i in range(points):
        p.append([random.uniform(0,100)-50 for j in range(dim)])
        p[i].append(random.sample(val,1)[0])
    return p 

testBias = True
count = 0
error = 0
total = 0
#samples = [[98,15,1],[20,81,1],[30,98,-1]]
samples = [[1,2,1],[2,3,-1],[3,1,1]]
if testBias:
    percep = perceptron(samples,1000,0.1)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
for i in range(1000):
    samples = randomPoints(2,3)
    percep = perceptron(samples,100000,0.1)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
print("count/total: ",count,"/",total)
if(error):
    print("errors: ",error)


