import random
import sys
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

def weightToStr(percep,method):
    output = ""
    if method == "standard":
        return str(percep.w) + " bias: " + str(percep.bias)
    if method == "voted":
        for m in range(len(percep.w)):
            output += "count"+ str(percep.c[m])+"["
            for wi in range(len(percep.w[m])):
                output += str(percep.w[m][wi])[:5] + ","
            output += "] bias: " + str(percep.bias[m])[:5] + "\n"
    if method == "average":
        for m in range(len(percep.archive)):
            output += "["
            for wi in range(len(percep.archive[m])):
                output +=  str(percep.archive[m][wi])[:5] + ","
            output += "] bias: " + str(percep.archivebias[m])[:5] + "\n"
    return output

    
def testAlgorithm(method,epochs):
    
    total = 0
    error = 0
    count = 0
    samples = sys.argv[1]
    #samples = "bank-note\\train.csv"
    percep = perceptron(samples,epochs,0.1,updateOn=method)
    samples = processCSV(samples)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(method," training ",epochs," error/total: ",error,"/",total)
    output = str(epochs) +","+ str((error+0.000001)/total)[:5]
    

    total = 0
    error = 0
    count = 0
    
    #samples = processCSV("bank-note\\test.csv");
    samples = processCSV(sys.argv[2]);
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(method," testing ",epochs," error/total: ",error,"/",total)
    output += "," + str((error+0.000001)/total)[:5]

    print(method," weights\n", weightToStr(percep,method),"\n bias: ", str(percep.bias),"\n")
    if(method == "average"):
        output += "\n\"" + str(percep.a) + "\"," + str(percep.abias)
        output += weightToStr(percep,method)
        #for i in range(len(percep.archive)):
            #output += "\narchive\n\"" + str(percep.archive[i]) + "\"," + str(percep.archivebias[i])
    else:
        output += "\n\"" + weightToStr(percep,method) + "\""
    
    return output

testingMethod = "voted"
testBias = False
bigTest = False
count = 0
error = 0
total = 0
#samples = [[98,15,1],[20,81,1],[30,98,-1]]

if testBias:
    samples = [[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1],[1,2,1],[2,3,0],[3,1,1]]
    percep = perceptron(samples,10,0.1,testingMethod)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(testingMethod," bias1: (",count,"/",total,")")
    samples = [[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0]]
    percep = perceptron(samples,20,0.1)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(testingMethod," biasfull: (",count,"/",total,")")
if bigTest:
    for i in range(1000):
        samples = randomPoints(2,3)
        percep = perceptron(samples,100,0.1,testingMethod)
        for j in range(len(samples)):
            pred = percep.prediction(samples[j])
            if samples[j][len(samples[j])-1] == pred:
                count += 1
            else:
                error += 1
            total +=1
    print("count/total: ",count,"/",total)
    

if len(sys.argv) == 1:
    print ("you did not provide testing or training file")
    quit()
if len(sys.argv) == 2:
    print ("you did not provide testing file")
    quit()

for method in ["standard","voted","average"]:
    output = method + "\nepochs,train,test\n"
    
        
    output += testAlgorithm(method,10) + "\n"
    
    file = open(method + "weight.csv","w")
    file.write(output)
    file.close() 



