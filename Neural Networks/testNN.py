import random
import sys
from proccessFiles import processCSV
from neuralNetwork import NNet
from neuralNetwork import splitExamples
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

def weightToStr(nNet,method):
    output = ""
    if method == "standard":
        return str(nNet.w) + " bias: " + str(nNet.bias)
    if method == "voted":
        for m in range(len(nNet.w)):
            output += "count"+ str(nNet.c[m])+"["
            for wi in range(len(nNet.w[m])):
                output += str(nNet.w[m][wi])[:5] + ","
            output += "] bias: " + str(nNet.bias[m])[:5] + "\n"
    if method == "average":
        for m in range(len(nNet.archive)):
            output += "["
            for wi in range(len(nNet.archive[m])):
                output +=  str(nNet.archive[m][wi])[:5] + ","
            output += "] bias: " + str(nNet.archivebias[m])[:5] + "\n"
    return output

    
def testAlgorithm(width,epochs,initW):
    
    total = 0
    error = 0
    count = 0
    samples = sys.argv[1]
    #samples = "bank-note\\train.csv"
    nNet = NNet(samples,10,0.1,2,width,initW)
    samples = processCSV(samples)
    split = splitExamples(samples)
    for i in range(len(samples)):
        x = split[0][i]
        y = split[1][i]
    

    
        pred = nNet.prediction(x)
        if pred * y > 0:
            count += 1
        else:
            error += 1
        total +=1
    print("width ",width," training ",epochs," error/total: ",error,"/",total)
    output = str(epochs) +","+ str((error+0.000001)/total)[:5]
    

    total = 0
    error = 0
    count = 0
    
    #samples = processCSV("bank-note\\test.csv");
    samples = processCSV(sys.argv[2]);
    split = splitExamples(samples)
    for i in range(len(samples)):
        x = split[0][i]
        y = split[1][i]
        pred = nNet.prediction(x)
        if pred*y > 0:
            count += 1
        else:
            error += 1
        total +=1
    print("width ",width," testing ",epochs," error/total: ",error,"/",total)
    output += "," + str((error+0.000001)/total)[:5]


    
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
    nNet = NNet(samples,10,0.1,testingMethod)
    for j in range(len(samples)):
        pred = nNet.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(testingMethod," bias1: (",count,"/",total,")")
    samples = [[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0],[-1,-2,0],[-2,-3,1],[-3,-1,0]]
    nNet = NNet(samples,20,0.1)
    for j in range(len(samples)):
        pred = nNet.prediction(samples[j])
        if samples[j][len(samples[j])-1] == pred:
            count += 1
        else:
            error += 1
        total +=1
    print(testingMethod," biasfull: (",count,"/",total,")")
if bigTest:
    for i in range(1000):
        samples = randomPoints(2,3)
        nNet = NNet(samples,100,0.1,testingMethod)
        for j in range(len(samples)):
            pred = nNet.prediction(samples[j])
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


for width in [5,10,25,50,100]:
    "w == rand"
    output = "w" + str(width) + " random\nepochs,train,test\n"
    output += testAlgorithm(width,10,True) + "\n"
    
    file = open("w" + str(width) + "randomWeight.csv","w")
    file.write(output)
    file.close() 
    
    "w == 0"
    output = "w" + str(width) + " weight=0\nepochs,train,test\n"
    output += testAlgorithm(width,10,False) + "\n"
    
    file = open("w" + str(width) + "zeroWeight.csv","w")
    file.write(output)
    file.close() 



