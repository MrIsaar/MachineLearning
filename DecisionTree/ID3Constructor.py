from proccessFiles import proccesDesc, processCSV
from ID3 import *


"""returns True if all labels in examples are the same"""
def allSameLabel(examples,columns,labels):
    labelIndex = columns.index("label")
    label = ""
    for example in examples:
        currLabel = example[labelIndex]
        if not labels.__contains__(currLabel):
            raise Exception("Label Not valid: " + currLabel)
        if label == "":
            label = currLabel
        else:
            if label != currLabel:
                return False
    return True

"""returns the most common label in examples that exists in the labels list"""
def MostCommonLabel(examples,columns,labels):
    labelIndex = columns.index("label")
    MCL = ""
    maxcount = 0
    lableOccurances = {}
    for example in examples:
        currLabel = example[labelIndex]
        if not labels.__contains__(currLabel):
            raise Exception("Not a valid Label: " + currLabel)
        if not lableOccurances.__contains__(currLabel):
            lableOccurances[currLabel] = 0
        lableOccurances[currLabel] +=1
        if lableOccurances[currLabel] > maxcount:
            maxcount = lableOccurances[currLabel]
            MCL = currLabel   
    return MCL

"""
    calculates gain based on provided gain method
    ie entropy, majority error, gini index 
"""
def gain(examples,attributes,attribute,columns,labels,gainMethod):
    # gain(S,A)=gainMethod(S) - sum( (|Sv|/|S|)* gainMethod(Sv))
    base = gainMethod(examples,labels,columns)
    expected = 0.0
    for Avalue in attributes[attribute]:
        exampleSubset = subsetExamples(examples,columns,attribute,Avalue)
        expected += ((len(exampleSubset)* 1.0) / len(examples))*gainMethod(exampleSubset,labels,columns)
    
    return base - expected

"""
    returns attribute to split on
"""
def splitOn(examples,attributes,columns,labels,gainMethod):
    maxgain = -1.0
    maxAttribute = ""
    if(len(examples) == 0):
        raise Exception("No Examples given")
    for attribute in attributes:
       currgain = gain(examples,attributes,attribute,columns,labels,gainMethod)
       if currgain > maxgain:
           maxgain = currgain
           maxAttribute = attribute
    
    return maxAttribute

"""creates a subset of the examples list that only has """
def subsetExamples(examples,columns,Attributename,A):
    AIndex = columns.index(Attributename)
    subset = []
    for sample in examples:
        if sample[AIndex] == A:
            subset.append(sample)
    return subset

"""
    subset of attributes dictonary except specified attribute
    Attributes - attribute
"""
def subsetAttributes(attributes,attribute):
    subset = attributes.copy()
    del subset[attribute]
    return subset



"""
    sets up algorithm and reads input files
    requires CSVfile and data description file as specified by proccessFiles
    maxdepth = -1 means that no limit is set
"""
def ID3setup(CSVfile,dataDescFile,gainMethod,maxdepth):
    description = proccesDesc(dataDescFile)
    examples = processCSV(CSVfile)
    attributes = description["attributes"]
    columns = description["columns"]
    labels = description["label values"]
    label = MostCommonLabel(examples,columns,labels)
    
    tree = ID3work(examples,label,attributes,columns,labels,gainMethod,maxdepth)
    return ID3Tree(tree, columns)


"""recursive that will return root node of subtree """
def ID3work(examples,label,attributes,columns,labels,gainMethod,maxdepth):
    if allSameLabel(examples,columns,labels):
        return Node(label)
    else:
        Attribute = splitOn(examples,attributes,columns,labels,gainMethod)
        root = Node("",Attribute,{})
        for branch in attributes[Attribute]:
            exampleSubset = subsetExamples(examples,columns,Attribute,branch)
            if len(exampleSubset ) == 0 or maxdepth  0:
                return Node(label)
            else:
                attributeSubset = subsetAttributes(attributes,Attribute)
                root.next[branch] = (ID3work(exampleSubset,MostCommonLabel(exampleSubset,columns,labels),attributeSubset,columns,labels,gainMethod,maxdepth-1))
        return root

class ID3Tree:
    def __init__(self,tree, columns,label="ID3Tree"):
        self.label = label
        self.columns = columns
        self.tree = tree

class Node:
    def __init__(self,label,attribute="label",next=None):
        self.label = label
        self.attribute = attribute
        self.next = next

if __name__ == '__main__':
    CSVfile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/train.csv"
    dataDescFile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/data-desc.txt"
    ID3setup(CSVfile,dataDescFile,entropy)