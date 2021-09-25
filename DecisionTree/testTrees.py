from proccessFiles import proccesDesc
from proccessFiles import processCSV
from ID3 import *
from sys import platform
import os



"""
    set up file connection to carfiles
"""
def carfiles(filenameEnd):
    dirname =  os.getcwd()
    carTrainFile = ""
    carDescriptFile = ""
    if dirname.endswith("DecisionTree"):
        dirname = os.path.dirname(dirname)
    if platform == "linux" or platform == "linux2":
       # carTrainFile = dirname + "/car/train.csv"
       # carDescriptFile = dirname + "/car/data-desc.txt"
       return dirname + "/car/" + filenameEnd
    else:
      # carTrainFile = dirname + "\\car\\train.csv"
      # carDescriptFile = dirname + "\\car\\data-desc.txt"
      return dirname + "\\car\\" + filenameEnd

"""
    set up file connection to bankfiles
"""      
def bankfiles(filenameEnd):
    dirname =  os.getcwd()
    carTrainFile = ""
    carDescriptFile = ""
    if dirname.endswith("DecisionTree"):
        dirname = os.path.dirname(dirname)
    if platform == "linux" or platform == "linux2":
       # carTrainFile = dirname + "/car/train.csv"
       # carDescriptFile = dirname + "/car/data-desc.txt"
       return dirname + "/bank/" + filenameEnd
    else:
      # carTrainFile = dirname + "\\car\\train.csv"
      # carDescriptFile = dirname + "\\car\\data-desc.txt"
      return dirname + "\\bank\\" + filenameEnd
carTrainFile = carfiles("train.csv")
carTestFile = carfiles("test.csv")
carDescriptFile = carfiles("data-desc.txt")

carTrainExamples = processCSV(carTestFile)
carTestExamples = processCSV(carTestFile)
carDescription = proccesDesc(carDescriptFile)

bankTrainFile = bankfiles("train.csv")
bankTestFile = bankfiles("test.csv")
bankDescriptFile = bankfiles("data-desc.txt")

bankTrainExamples = processCSV(bankTrainFile)
bankTestExamples = processCSV(bankTestFile)
bankDescription = proccesDesc(bankDescriptFile)



"""builds tree based on """
def testTrain(calc,examples,maxdepth=-1,carExamples=True,handleUnknown=False):
    tree = None
    attributes = None
    columns = None
    labels = None

    if(carExamples == True):
        tree = ID3(carTrainFile,carDescriptFile,maxdepth,calc)
        attributes = carDescription["attributes"]
        columns = carDescription["columns"]
        labels = carDescription["label values"]

    else:
        tree =ID3(bankTrainFile,bankDescriptFile,maxdepth,calc,handleUnknown)
        attributes = bankDescription["attributes"]
        columns = bankDescription["columns"]
        labels = bankDescription["label values"]

    
    wrongPredict = 0
    totalSamples = 0
    for sample in examples:
        result = getResult(tree,sample)
        totalSamples +=1
        if result != sample[len(sample)-1]:
            wrongPredict += 1
    percent = ((totalSamples-wrongPredict *1.0)/totalSamples+0.00001)
    #print("MaxDepth "+str(maxdepth)+" " + str(totalSamples-wrongPredict) + "/" + str(totalSamples) + " for " + str(percent)[2:4] + "."+str(percent)[4:5]+"% on training data ")
    return str(percent)


#training car data
header = "car Training"
output = "InfoGain"
for i in range(7):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",carTrainExamples,i))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(7):
    output += "\t" + str(testTrain("majority error",carTrainExamples,i))[:5]
print(output)
output = "GiniIndex"
for i in range(7):
    output += "\t" + str(testTrain("gini index",carTrainExamples,i))[:5]
print(output)


#test car data
header = "car Testing"
output = "InfoGain"
for i in range(7):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",carTestExamples,i))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(7):
    output += "\t" + str(testTrain("majority error",carTestExamples,i))[:5]
print(output)
output = "GiniIndex"
for i in range(7):
    output += "\t" + str(testTrain("gini index",carTestExamples,i))[:5]
print(output)


#training bank data
header = "\nBank Training unknown as value"
output = "InfoGain"
for i in range(16):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",bankTrainExamples,i,False))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(16):
    output += "\t" + str(testTrain("majority error",bankTrainExamples,i,False))[:5]
print(output)
output = "GiniIndex"
for i in range(16):
    output += "\t" + str(testTrain("gini index",bankTrainExamples,i,False))[:5]
print(output)

#test bank data
header = "\nbank Testing  unknown as value"
output = "InfoGain"
for i in range(16):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",bankTestExamples,i,False))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(16):
    output += "\t" + str(testTrain("majority error",bankTestExamples,i,False))[:5]
print(output)
output = "GiniIndex"
for i in range(16):
    output += "\t" + str(testTrain("gini index",bankTestExamples,i,False))[:5]
print(output)


#training bank data
header = "\nBank Training unknown prediction"
output = "InfoGain"
for i in range(16):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",bankTrainExamples,i,False,True))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(16):
    output += "\t" + str(testTrain("majority error",bankTrainExamples,i,False,True))[:5]
print(output)
output = "GiniIndex"
for i in range(16):
    output += "\t" + str(testTrain("gini index",bankTrainExamples,i,False,True))[:5]
print(output)

#test bank data
header = "\nbank Testing  unknown prediction"
output = "InfoGain"
for i in range(16):
    header += "\t" + str(i)
    output += "\t" + str(testTrain("information gain",bankTestExamples,i,False,True))[:5]
print (header)
print(output)
output = "MajorError"
for i in range(16):
    output += "\t" + str(testTrain("majority error",bankTestExamples,i,False,True))[:5]
print(output)
output = "GiniIndex"
for i in range(16):
    output += "\t" + str(testTrain("gini index",bankTestExamples,i,False,True))[:5]
print(output)
"""
"""