import random
import sys
import math
from proccessFiles import processCSV
from svm import svm
import threading

def progressBar(prog,maxProg,size=20):
    if prog % math.floor(maxProg/size) == 0 or prog == maxProg:
        percent = (prog + 0.0001)/maxProg
        update = "|"
        for j in range(math.floor((prog*size)/maxProg)):
            update += "#"
        for j in range(math.floor(size - math.floor((prog/maxProg)*size))):
            update += " "
        if percent < 0.001:
            percent = "00.0"
        elif percent >= 0.99:
            percent = "100.0"
        else:
            percent = str((prog + 0.0001)/maxProg)[2:4] + "." + str((prog + 0.0001)/maxProg)[4:5]
        update += "|" + percent + "%"
        sys.stdout.write("\r"+update)
        sys.stdout.flush()
    if prog == maxProg:
        sys.stdout.write("\n")
        sys.stdout.flush()
        

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
    
    return str(percep.w) 
    

def testAlgorithm(method,epochs,c,learninga):
    
    output = 0
    total = 0
    error = 0
    count = 0
    samples = sys.argv[1]
    #samples = "bank-note\\train.csv"
    
    percep = svm(samples,10,0.1,learninga,c,method)
    samples = processCSV(samples)
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] * pred >= 0:
            count += 1
        else:
            error += 1
        total +=1
    #print(method," training ",epochs," error/total: ",error,"/",total)
    #output = str(epochs) +","+ str((error+0.000001)/total)[:5]
    
    output = error / total
    
    total = 0
    error = 0
    count = 0
    
    #samples = processCSV("bank-note\\test.csv");
    samples = processCSV(sys.argv[2]);
    for j in range(len(samples)):
        pred = percep.prediction(samples[j])
        if samples[j][len(samples[j])-1] * pred >= 0:
            count += 1
        else:
            error += 1
        total +=1
    #print(method," testing ",epochs," error/total: ",error,"/",total)
    #output += "," + str((error+0.000001)/total)[:5]

    #print(method," weights\n", weightToStr(percep,method),"\n")
    
    #output += "\n\"" + weightToStr(percep,method) + "\""
    output = (output,(error /total))
    
    return output

def test(hyper,out,learninga,algorithm):
    output = "c="+ str(math.ceil(hyper*873))[:3] + "/873" + "\nepochs,train,test\n"
    count = 0
    trainErr = 0
    testErr = 0
    testsize = 20
    
    for i in range(testsize):
        count+=1
        trer,tser = testAlgorithm(algorithm,10,hyper,learninga)
        #progressBar(i + testsize*c.index(hyper),testsize*len(c),40)
        trainErr += trer
        testErr += tser
        if i % math.floor(testsize/4.0) == 0:
            print(algorithm,": ", i,"/",testsize, " hyper: " , math.ceil(hyper*873),"/873")
    output += "10," + str(trainErr/count)+","+str(testErr/count)  + "\n"
    updateOut(output,out)




threadLock = threading.Lock()
threads = []

c = [(100/873),(500/873),(700/873)]
learninga = 2
output = []

def updateOut(out,output):
    threadLock.acquire()
    output.append(out)
    threadLock.release()
    
  
print("starting SGD")  
for hyper in c:
    """multithread testing for faster results"""
    thread = threading.Thread(target=test,args=(hyper,output,learninga,"sgd"))
    thread.start()
    
    threads.append(thread)
    """
    output += "c="+ str(hyper*873)[:-2] + "/873" + "\nepochs,train,test\n"
    count = 0
    trainErr = 0
    testErr = 0
    testsize = 50
    
    for i in range(testsize):
        count+=1
        trer,tser = testAlgorithm("sgd",10,hyper)
        progressBar(i + testsize*c.index(hyper),testsize*len(c),40)
        trainErr += trer
        testErr += tser
    output += "10," + str(trainErr/count)+","+str(testErr/count)  + "\n"
   
"""

#progressBar(40,40,40)
for thread in threads:
    thread.join()
print(output)
file = open("sgd" + "weight.csv","w")
for out in output:
    if out.startswith("sgd"):
        file.write(str(out))
file.close() 

output = []

print ("starting dual")
""" DUAL  """
for hyper in c:
    """multithread testing for faster results"""
    thread = threading.Thread(target=test,args=(hyper,output,learninga,"dual"))
    thread.start()
    
    threads.append(thread)
    """
    output += "c="+ str(hyper*873)[:-2] + "/873" + "\nepochs,train,test\n"
    count = 0
    trainErr = 0
    testErr = 0
    testsize = 50
    
    for i in range(testsize):
        count+=1
        trer,tser = testAlgorithm("sgd",10,hyper)
        progressBar(i + testsize*c.index(hyper),testsize*len(c),40)
        trainErr += trer
        testErr += tser
    output += "10," + str(trainErr/count)+","+str(testErr/count)  + "\n"
    """
#progressBar(40,40,40)
for thread in threads:
    thread.join()
print(output)
"""
file = open("sgd" + "weight.csv","w")
for out in output:
    if out.startswith("sgd"):
        file.write(str(out))
file.close() 
"""
file = open("dual" + "weight.csv","w")
for out in output:
    
    if out.startswith("dual"):
        file.write(str(out))
file.close() 