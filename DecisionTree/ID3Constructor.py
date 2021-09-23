from proccessFiles import proccesDesc, processCSV
from ID3 import *

CSVfile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/train.csv"

dataDescFile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/data-desc.txt"
"""
    sets up algorithm and reads input files
    requires CSVfile and data description file as specified by proccessFiles
    maxdepth = -1 means that no limit is set
"""
def ID3setup(CSVfile,dataDescFile,gainMethod,maxdepth=-1):
    description = proccesDesc(dataDescFile)
    examples = processCSV(CSVfile)
    attributes = description["attributes"]
    columns = description["columns"]
    labels = description["label values"]
    label = MostCommonLabel(examples,columns,labels)
    ID3(examples,label,attributes,columns,labels,gainMethod,maxdepth)


"""recursive that will return root node of subtree """
def ID3(examples,label,attributes,columns,labels,gainMethod,maxdepth):
    if allSameLabel(examples,columns,labels,attributes) == False:
        return Node(label)
    else:
        A = splitOn(examples,attributes,columns,gainMethod)
        root = Node(A,[])
        for branch in attributes[A]:
            exampleSubset = subsetExamples(examples,columns,A,branch)
            if len(exampleSubset ) == 0 or maxdepth == 0:
                return Node(label)
            else:
                attributeSubset = subsetAttributes(attributes,A)
                root.next.append(ID3(exampleSubset,label,attributes,columns,labels,gainMethod,maxdepth-1))
        return root


def allSameLabel(examples,columns,labels,attributes):
    [1,2,"label"].index("label")
    return False

def MostCommonLabel(examples,columns,labels):
    return ""

def splitOn(examples,attributes,columns,gainMethod):
    return gainMethod(examples,attributes,columns)

def subsetExamples(examples,columns,A,branch):
    return "not done"

def subsetAttributes(attributes,A):
    return "not done"



class Node:
    def __init__(self,label,next=None):
        self.label = label
        self.next = next

if __name__ == '__main__':
    ID3setup(CSVfile,dataDescFile,)