import random
import math
from proccessFiles import proccesDesc,processCSV
from ID3 import ID3,getResult,entropy
from ID3Constructor import ID3work,MostCommonLabel,solveNumberic,ID3Tree,splitOn,subsetAttributes,Node,subsetExamples

"""
    uniformily selects from the list of samples with replacement and returns a list

"""
def uniformSample(samples,size=-1):
    m = len(samples)
    if size != -1:
        m = int(math.floor(size))
    samplelist = []
    
    for i in range(m):
        j = math.floor(random.uniform(0,m))
        

        samplelist.append(samples[j])
    
    return samplelist

def uniformAttribute(attributes,size):
    keys = []
    size = int(math.floor(size))
    attributesSub = attributes.copy()
    atr = {}
    for a in attributes.keys():
        keys.append(a)
    for i in range(size):
        j = math.floor(random.uniform(0,len(attributesSub)))
        key = keys.pop(j)
        atr[key] = (attributesSub.pop(key))
        
    return atr



class Forest():
    def __init__(self,CSVfile,dataDescFile,T):
        self.description = proccesDesc(dataDescFile)
        self.T = T
        self.examples = processCSV(CSVfile)
        self.csv = CSVfile
        self.dataDesc = dataDescFile
        self.labels = self.description["label values"]
        self.columns = self.description["columns"]
        self.attributes = self.description["attributes"]
        self.attributes = solveNumberic(self.examples,self.attributes,self.columns)
        self.createForest()

    """
     creates forest using the Random Forest algorithm found on pg 90
    """
    def createForest(self):
        forest= []
        for t in range(self.T):
            samples = uniformSample(self.examples)
            forest.append(ID3Tree(self.RandTreeLearn(samples,self.attributes), self.columns,self.attributes))
        self.forest = forest

    """
        RandTreeLearn(Xt,Yt,F) where F is stored in self
    """
    def RandTreeLearn(self, samples,attributes):
        tree = ID3work(samples,MostCommonLabel(samples,self.columns,self.labels),attributes,self.columns,self.labels,entropy,2,True)
        return tree
        """
        attributesSub = uniformAttribute(attributes,len(attributes)/4 + 1)
        split = splitOn(samples,attributesSub,self.columns,self.labels,entropy,True)
        root = Node("",split,{})
        
        for branch in attributes[split]:
            exampleSubset = subsetExamples(samples,self.columns,split,branch,True)
            if len(exampleSubset ) == 0:
                return Node(MostCommonLabel(samples,self.columns,self.labels))
            else:
                attributeSubset = subsetAttributes(attributes,split)
                root.next[branch] = self.RandTreeLearn(exampleSubset,attributeSubset)
        return root
        """

    """
        returns prediction based on sample
    """
    def Result(self,sample):
        sum = 0
        for t in range(self.T):
            sum += self.labelTranslate(getResult(self.forest[t],sample))
        sum /= self.T
        if(sum < 0):
                #negative option
            return self.labels[0]
        if(sum > 0):
                #positive option
            return self.labels[1]
        return 0

    """ determines if the label is -1 or 1"""
    def labelTranslate(self,label):
        if type(label) is not str:
            return label
        if(label == self.labels[0]):
            return -1
        if(label == self.labels[1]):
            return 1

    def ExampleSubset(self,examples,attributesSub):
        attributes = []
        samples = []
        for attribute in attributesSub:
            
            for branch in self.attributes[attribute]:
                exampleSubset = subsetExamples(examples,self.columns,attribute,branch,True)
                for sample in exampleSubset:
                    samples.append(sample)
        return samples

        

    