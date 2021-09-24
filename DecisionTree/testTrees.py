from proccessFiles import proccesDesc
from proccessFiles import processCSV
from ID3 import *
from sys import platform
import os

"""
    set up file connection
"""
dirname =  os.getcwd()
if dirname.endswith("DecisionTree"):
    dirname = os.path.dirname(dirname)
if platform == "linux" or platform == "linux2":
        
    carTrainFile = dirname + "/car/train.csv"
    carDescriptFile = dirname + "/car/data-desc.txt"
else:
    carTrainFile = dirname + "\\car\\train.csv"
    carDescriptFile = dirname + "\\car\\data-desc.txt"
carExamples = processCSV(carTrainFile)
carDescription = proccesDesc(carDescriptFile)



def testTrain(maxdepth=-1):
    tree = ID3(carTrainFile,carDescriptFile,maxdepth)
    attributes = carDescription["attributes"]
    columns = carDescription["columns"]
    labels = carDescription["label values"]

    wrongPredict = 0
    totalSamples = 0
    for sample in carExamples:
        result = getResult(tree,sample)
        totalSamples +=1
        if result != sample[len(sample)-1]:
            wrongPredict += 1
    percent = ((totalSamples-wrongPredict *1.0)/totalSamples+0.00001)
    print("Decision tree is correct " + str(totalSamples-wrongPredict) + " / " + str(totalSamples) + " times for " + str(percent)[2:4] + "."+str(percent)[4:5]+"% on training data ")






for i in range(-1,7):
    print("test " + str(i) + "\n------")
    testTrain(i)