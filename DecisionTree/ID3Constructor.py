from proccessFiles import proccesDesc, processCSV
from ID3 import *

"""

find median example of list of numbers and index of number
"""
def findMedian(examples,index):
    allnumbers = []
    for example in examples:
        allnumbers.append(example[index])
    allnumbers.sort()
    return allnumbers[(math.floor(len(allnumbers)/2))]



"""processes numeric values to find median will return Attributes dictionary with adjusted values"""
def solveNumberic(examples,attributes,columns):
    changed = False
    newAttributes = {}
    for attribute in attributes:
        value = attributes[attribute][0]
        if value.startswith("<") and value.endswith(">"):
            index = columns.index(attribute)
            median = findMedian(examples,index)
            valueless = "<<" +str(median)+">"
            valuemore = "<>" +str(median)+">"
            newAttributes[attribute] = [valueless,valuemore]
            changed = True
        else:
            newAttributes[attribute] = attributes[attribute]
    if changed:
        return newAttributes
    else:
        return attributes


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


def MostCommonAttribute(examples,AIndex):
    MCL = "unknown"
    maxcount = 0
    lableOccurances = {}
    for example in examples:
        currLabel = example[AIndex]
        if currLabel == "unknown":
            continue
        if not lableOccurances.__contains__(currLabel):
            lableOccurances[currLabel] = 0
        lableOccurances[currLabel] +=1
        if lableOccurances[currLabel] > maxcount:
            maxcount = lableOccurances[currLabel]
            MCL = currLabel   
    return MCL

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
def gain(examples,attributes,attribute,columns,labels,gainMethod,handleUnknown):
    # gain(S,A)=gainMethod(S) - sum( (|Sv|/|S|)* gainMethod(Sv))
    base = gainMethod(examples,labels,columns)
    expected = 0.0
    for Avalue in attributes[attribute]:
        exampleSubset = subsetExamples(examples,columns,attribute,Avalue,handleUnknown)
        expected += ((len(exampleSubset)* 1.0) / len(examples))*gainMethod(exampleSubset,labels,columns)
    
    return base - expected

"""
    returns attribute to split on
"""
def splitOn(examples,attributes,columns,labels,gainMethod,handleUnknown):
    maxgain = -1.0
    maxAttribute = ""
    if(len(examples) == 0):
        raise Exception("No Examples given")
    for attribute in attributes:
       currgain = gain(examples,attributes,attribute,columns,labels,gainMethod,handleUnknown)
       if currgain > maxgain:
           maxgain = currgain
           maxAttribute = attribute
    
    return maxAttribute

"""creates a subset of the examples list that only has """
def subsetExamples(examples,columns,Attributename,A,handleUnknown):
    AIndex = columns.index(Attributename)
    subset = []
    numeric = False
    if A.startswith("<") and A.endswith(">") and len(A) > 3:
            A = A[1:len(A)-1]
            numeric = True
    MCA = ""
    if handleUnknown:
        MCA = MostCommonAttribute(examples,AIndex)
    for sample in examples:
        if numeric:
            if A[:1] =="<":
                if float(sample[AIndex]) < float(A[1:]):
                    subset.append(sample)
            else:
                if float(sample[AIndex]) >= float(A[1:]):
                    subset.append(sample)
         
        else:
            if sample[AIndex] == "unknown" and handleUnknown:
                
                if MCA == A:
                    subset.append(sample)
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
def ID3setup(CSVfile,dataDescFile,gainMethod,maxdepth,handleUnknown):
    description = proccesDesc(dataDescFile)
    examples = processCSV(CSVfile)
    attributes = description["attributes"]
    columns = description["columns"]
    labels = description["label values"]
    label = MostCommonLabel(examples,columns,labels)
    attributes = solveNumberic(examples,attributes,columns)
    
    tree = ID3work(examples,label,attributes,columns,labels,gainMethod,maxdepth,handleUnknown)
    return ID3Tree(tree, columns,attributes)


"""recursive that will return root node of subtree """
def ID3work(examples,label,attributes,columns,labels,gainMethod,maxdepth,handleUnknown):
    if allSameLabel(examples,columns,labels):
        return Node(label)
    else:
        Attribute = splitOn(examples,attributes,columns,labels,gainMethod,handleUnknown)
        root = Node("",Attribute,{})
        for branch in attributes[Attribute]:
            exampleSubset = subsetExamples(examples,columns,Attribute,branch,handleUnknown)
            if len(exampleSubset ) == 0 or maxdepth == 0:
                return Node(label)
            else:
                attributeSubset = subsetAttributes(attributes,Attribute)
                root.next[branch] = (ID3work(exampleSubset,MostCommonLabel(exampleSubset,columns,labels),attributeSubset,columns,labels,gainMethod,maxdepth-1,handleUnknown))
        return root

class ID3Tree:
    def __init__(self,tree, columns,attributes,label="ID3Tree"):
        self.label = label
        self.columns = columns
        self.tree = tree
        self.attributes = attributes

class Node:
    def __init__(self,label,attribute="label",next=None):
        self.label = label
        self.attribute = attribute
        self.next = next

if __name__ == '__main__':
    CSVfile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/train.csv"
    dataDescFile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/data-desc.txt"
    ID3setup(CSVfile,dataDescFile,entropy)