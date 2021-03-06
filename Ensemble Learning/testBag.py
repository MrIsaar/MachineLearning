from proccessFiles import proccesDesc
from proccessFiles import processCSV
from sys import platform
from AdaBoost import AdaBoost
from Bagging import bagging
from forest import Forest
import os

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



TrainFile = genericfiles("small","train.csv")
TestFile = genericfiles("small","test.csv")
DescriptFile = genericfiles("small","data-desc.txt")
TrainExamples = processCSV(TrainFile)


function = AdaBoost(TrainFile,DescriptFile,5)
errors= 0
total= 0
for sample in TrainExamples: 
    testResult = function.Hfinal(sample)
    if (sample[len(sample)-1] != testResult ):
        errors += 1
    total +=1  
print("train small: ",errors , " errors out of ", total)




bankTrainFile = bankfiles("train.csv")
bankTestFile = bankfiles("test.csv")
bankDescriptFile = bankfiles("data-desc.txt")

bankTrainExamples = processCSV(bankTrainFile)
bankTestExamples = processCSV(bankTestFile)
bankDescription = proccesDesc(bankDescriptFile)

output = ""


print("-,train,Test")
fullOut = "-,train,Test\n"
for t in range(1,500):

    function = AdaBoost(bankTrainFile,bankDescriptFile,t)
    output = "" + str(t) 
    errors= 0
    total= 0
    for sample in bankTrainExamples: 
        testResult = function.Hfinal(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]

    errors= 0
    total= 0
    for sample in bankTestExamples: 
        testResult = function.Hfinal(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("test: ", errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]
    print (output)
    fullOut += output + "\n"

file = open(genericfiles("results","bankboostResults.txt"),"w")
file.write(fullOut)
file.close()



print("Small Training bagging")
output = ""
for t in range(1,5):
    bag = bagging(TrainFile,DescriptFile,t)
    output = "" + str(t)
    errors= 0
    total= 0
    for sample in TrainExamples: 
        testResult = bag.bagResult(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]
print(output)


print("bank Training")
fullOut = ""
for t in range(1,500):
    bag = bagging(bankTrainFile,bankDescriptFile,t)
    output = "" + str(t)
    errors= 0
    total= 0
    for sample in bankTrainExamples: 
        testResult = bag.bagResult(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5] 
    errors= 0
    total= 0
    for sample in bankTestExamples: 
        testResult = bag.bagResult(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]
    fullOut += output + "\n"
    print(output)
file = open(genericfiles("results","bankbagResults.txt"),"w")
file.write(fullOut)
file.close()  


print("Small Training forest")
output = ""
for t in range(1,5):
    forest = Forest(TrainFile,DescriptFile,t)
    output = "" + str(t)
    errors= 0
    total= 0
    for sample in TrainExamples: 
        testResult = forest.Result(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]
print(output)



print("forest Training")
fullOut = ""
for t in range(1,500):
    tree = Forest(bankTrainFile,bankDescriptFile,t)
    output = "" + str(t)
    errors= 0
    total= 0
    for sample in bankTrainExamples: 
        testResult = tree.Result(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5] 
    errors= 0
    total= 0
    for sample in bankTestExamples: 
        testResult = tree.Result(sample)
        if (sample[len(sample)-1] != testResult ):
            errors += 1
        total +=1  
    #print("train: ",errors , " errors out of ", total)
    output += "," + str(1-(errors/total))[:5]
    fullOut += output + "\n"
    print(output)
file = open(genericfiles("results","bankforestResults.txt"),"w")
file.write(fullOut)
file.close() 