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
    learningrate = 0.1
    if method == "kernal":
        learningrate = learninga
    #samples = "bank-note\\train.csv"
    
    percep = svm(samples,10,learningrate,learninga,c,method)
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
    output = (output,(error /total),percep)
    
    return output

def test(hyper,out,learninga,algorithm,testsize=20):
    a = learninga
    if a == hyper:
        a = str(math.ceil(hyper*873))[:3] + "/873"
    output = str(algorithm)+" c="+ str(math.ceil(hyper*873))[:3] + "/873 a=" + str(a) + "\nepochs,train,test,weights\n"
    count = 0
    trainErr = 0
    testErr = 0
   
    
    for i in range(testsize):
        count+=1
        trer,tser,svm = testAlgorithm(algorithm,10,hyper,learninga)
        #progressBar(i + testsize*c.index(hyper),testsize*len(c),40)
        trainErr += trer
        testErr += tser
        if i % math.ceil(testsize/4.0) == 0:
            print(algorithm," progress: ", i,"/",testsize, " hyper: " , math.ceil(hyper*873),"/873")
    output += "10," + str(trainErr/count)+","+str(testErr/count) + "," + str(svm.w) + "\n"
    if algorithm == "kernal":
        for i in range(len(svm.alpha)):
            if svm.alpha[i] > 0.00001:
                output += str(svm.x[i])
        output += "\n"
    updateOut(output,out)


testSGD = True
testDual = True
testKernal = True

if len(sys.argv) == 4 and sys.argv[3] != "all":
    testSGD = sys.argv[3] == "sgd"
    testDual = sys.argv[3] == "dual"
    testKernal = sys.argv[3] == "kernal"

threadLock = threading.Lock()
threads = []

c = [(100/873),(500/873),(700/873)]
learninga = 2
output = []

def updateOut(out,output):
    threadLock.acquire()
    output.append(out)
    threadLock.release()
    
if(testSGD): 
    print("starting SGD")  
    for hyper in c:
        """multithread testing for faster results"""
        thread = threading.Thread(target=test,args=(hyper,output,learninga,"sgd"))
        thread.start() 
        threads.append(thread)
    
        thread = threading.Thread(target=test,args=(hyper,output,hyper,"sgd"))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(output)
    file = open("sgd" + "results.csv","w")
    for out in output:
        if out.startswith("sgd"):
            file.write(str(out))
    file.close() 



if(testDual):
    output = []
    print ("starting dual: warning takes a long time")
    """ DUAL  """
    for hyper in c:
        """multithread testing for faster results"""
        thread = threading.Thread(target=test,args=(hyper,output,learninga,"dual",1))
        thread.start()
    
        threads.append(thread)
  

    for thread in threads:
        thread.join()
    print(output)

    file = open("dual" + "results.csv","w")
    for out in output:
    
        if out.startswith("dual"):
            file.write(str(out))
    file.close() 
 
    
if(testKernal):
    output = []
    learnList = [0.1,0.5,1,5,100]
    print ("starting kernal: warning takes a long time")
    """ KERNAL  """
    for hyper in c:
        for learn in learnList:
            """multithread testing for faster results"""
            thread = threading.Thread(target=test,args=(hyper,output,learn,"kernal",1))
            thread.start()
    
            threads.append(thread)
  
    #progressBar(40,40,40)
    for thread in threads:
        thread.join()
    print(output)

    file = open("kernal" + "results.csv","w")
    for out in output:
    
        if out.startswith("kernal"):
            file.write(str(out))
    file.close() 