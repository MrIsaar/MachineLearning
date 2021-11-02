import random
from proccessFiles import processCSV
from perceptron import perceptron
def randomPoints(dim,points):
    val = [0,1]
    p = []
    for i in range(points):
        p.append([random.uniform(0,100)-50 for j in range(dim)])
        p[i].append(random.sample(val,1)[0])
    i = len(p)
    for point in p:
        p.append(point);
        if i < 0:
            break
        i-=1
    return p 

def testAlgorithm(method,epochs):
    
    total = 0
    error = 0
    count = 0
    samples = "bank-note\\train.csv"
    percep = perceptron(samples,epochs,0.1,updateOn=method)
    samples = processCSV(samples)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(method," training count/total: ",count,"/",total)
    output = str(epochs) +","+ str(count/total)[:-5] 

    total = 0
    error = 0
    count = 0
    
    samples = processCSV("bank-note\\test.csv");
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(method," testing count/total: ",count,"/",total)
    output += str(count/total)[:-5]
    return output

testBias = False
bigTest = False
count = 0
error = 0
total = 0
#samples = [[98,15,1],[20,81,1],[30,98,-1]]

if testBias:
    samples = [[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1]]
    percep = perceptron(samples,10,0.1)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1

    samples = [[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0]]
    percep = perceptron(samples,20,0.1)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
if bigTest:
    for i in range(1000):
        samples = randomPoints(2,3)
        percep = perceptron(samples,100,0.1)
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



for method in ["standard","voted","average"]:
    for i in range(10):
        output = method + "\nepochs,train,test\n"
        output += testAlgorithm(method,i+1) + "\n"
    
    file = open(method + "Results.csv","w")
    file.write(output)
    file.close() 


