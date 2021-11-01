from proccessFiles import proccesDesc
from proccessFiles import processCSV
from sys import platform
from gradient import gradent,strtofloat
import os

def genericfiles(folder,filenameEnd):
    dirname =  os.getcwd()
    carTrainFile = ""
    carDescriptFile = ""
    if dirname.endswith("DecisionTree"):
        dirname = os.path.dirname(dirname)
    if platform == "linux" or platform == "linux2":
       # carTrainFile = dirname + "/car/train.csv"
       # carDescriptFile = dirname + "/car/data-desc.txt"
       return dirname + "/"+folder+"/" + filenameEnd
    else:
      # carTrainFile = dirname + "\\car\\train.csv"
      # carDescriptFile = dirname + "\\car\\data-desc.txt"
      return dirname + "\\"+folder+"\\" + filenameEnd

smallLMSCSV= genericfiles("small","lmsTrain.csv")
concreteCSV = genericfiles("concrete","train.csv")
TrainExamples = strtofloat(processCSV(smallLMSCSV))
"""
small = gradent(smallLMSCSV,0.3,0.1)
error = 0
total = 0
for sample in TrainExamples:
    result = small.result(sample)
    answer = sample[len(sample)-1]
    if abs(result - answer) > 1:
        error += 1
    total += 1
print(str(error)+ " / "+str(total))
"""
concrete = gradent(concreteCSV,0.3,0.1)
error = 0
total = 0
for sample in TrainExamples:
    if abs(concrete.result(sample) - sample[len(sample)-1]) > 1:
        error += 1
    total += 1
print(str(error)+ " / "+str(total))
