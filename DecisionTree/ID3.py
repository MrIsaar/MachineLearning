from a01 import giniIndex
import math

"""
    calculates entropy for information gain 
    - sum ( plog2(p)  )
"""
def entropy(examples,labels,columns):
    if(len(examples) <= 1):
        return 0.0
    
    LIndex = columns.index("label")
    itemsSeen = 0
    entropyVal = 0
    labelDict = {}
    for example in examples:
        currlabel = example[LIndex]
        if not labels.__contains__(currlabel):
            raise Exception("label not in label list: " + currlabel)
        if not labelDict.__contains__(currlabel):
            labelDict[currlabel] = 0
        labelDict[currlabel] += 1
        itemsSeen += 1
    if itemsSeen != len(examples):
        raise Exception("entropy not same count something is wrong")


    for label in labelDict:
        p = labelDict[label]/itemsSeen
        curr = p * math.log(p,2)
        entropyVal += curr
        
    return -entropyVal


"""
    Majority Error
"""
def MajorityError(examples,labels,columns):
    if(len(examples) <= 1):
        return 0.0
    
    LIndex = columns.index("label")
    itemsSeen = 0
    majority = 0
    majorityLabel=""
    labelDict = {}
    for example in examples:
        currlabel = example[LIndex]
        if not labels.__contains__(currlabel):
            raise Exception("label not in label list: " + currlabel)
        if not labelDict.__contains__(currlabel):
            labelDict[currlabel] = 0
        labelDict[currlabel] += 1
        itemsSeen += 1
        if labelDict[currlabel] > majority:
            majority = labelDict[currlabel]
            majorityLabel = currlabel

    if itemsSeen != len(examples):
        raise Exception("entropy not same count something is wrong")
    
    return (itemsSeen - majority)/majority
        

"""
    creates decision tree using the ID3 algorithm and 
    requires a CSV file and description file to create 
    tree based on provided data.

    set gainCalculation to set which way of calculating gain with following inputs:
     "information gain","majority error", "gini index"
    will default to "information gain" if none are specified or invalid 
"""
def ID3(filename,descriptFile,gainCalculation="information gain"):
   
    if gainCalculation.lower() == "majority error":
        print( "using Majority Error")
        return ID3setup(filename,descriptFile,MajorityError)
    else:
        if gainCalculation.lower() == "gini index":
            print( "using gini index")
            return ID3setup(filename,descriptFile,giniIndex)
        else:
            print( "using information gain")
            return ID3setup(filename,descriptFile,entropy)



if __name__ == '__main__':
    from ID3Constructor import ID3setup
    from sys import platform
    import os

    dirname =  os.getcwd()
    dirname = os.path.dirname(dirname)
    if platform == "linux" or platform == "linux2":
        
        filename = dirname + '/car/train.csv'
        descriptFile = dirname + "/car/data-desc.txt"
    else:
        filename = dirname + '\\car\\train.csv'
        descriptFile = dirname + "\\car\\data-desc.txt"
    print(filename)
    print(descriptFile)
    tree = ID3setup(filename,descriptFile,MajorityError)
    print("done building tree")



    #os.sytem.args