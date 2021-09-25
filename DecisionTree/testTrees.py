from proccessFiles import proccesDesc
from proccessFiles import processCSV
from ID3 import *
from sys import platform
import os



"""
    set up file connection
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
    
carTrainFile = carfiles("train.csv")
carTestFile = carfiles("test.csv")
carDescriptFile = carfiles("data-desc.txt")

carTrainExamples = processCSV(carTestFile)
carTestExamples = processCSV(carTestFile)
carDescription = proccesDesc(carDescriptFile)

"""builds tree based on """
def testTrain(calc,examples,maxdepth=-1):
    tree = ID3(carTrainFile,carDescriptFile,maxdepth,calc)
    attributes = carDescription["attributes"]
    columns = carDescription["columns"]
    labels = carDescription["label values"]

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



header = "car Training"
output = "InfoGain"
for i in range(7):
    header += "," + str(i)
    output += "\t" + testTrain("information gain",carTrainExamples,i)
print (header)
print(output)
output = "MajorError"
for i in range(7):
    output += "\t" + testTrain("majority error",carTrainExamples,i)
print(output)
output = "GiniIndex"
for i in range(7):
    output += "\t" + testTrain("gini index",carTrainExamples,i)
print(output)

#test data
header = "car Testing"
output = "InfoGain"
for i in range(7):
    header += "\t" + str(i)
    output += "\t" + testTrain("information gain",carTestExamples,i)
print (header)
print(output)
output = "MajorError"
for i in range(7):
    output += "\t" + testTrain("majority error",carTestExamples,i)
print(output)
output = "GiniIndex"
for i in range(7):
    output += "\t" + testTrain("gini index",carTestExamples,i)
print(output)