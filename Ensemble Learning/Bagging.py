import random
import math
from proccessFiles import proccesDesc,processCSV
from ID3 import ID3,getResult,entropy
from ID3Constructor import ID3work,MostCommonLabel,solveNumberic,ID3Tree

class bagging():
    def __init__(self,CSVfile,dataDescFile,T=5):
        self.description = proccesDesc(dataDescFile)
        self.T = T
        self.examples = processCSV(CSVfile)
        self.csv = CSVfile
        self.dataDesc = dataDescFile
        
        self.bagwork()

    def bagResult(self,sample):
        sign = 0
        for t in range(self.T):  
            hi = self.labelTranslate(getResult(self.c[t],sample))
            sign += self.a[t]*hi
        if(sign < 0):
                #negative option
            return self.labels[0]
        if(sign > 0):
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

    """calculates error for voting"""
    def error(self,t):
        sum = 0
        for i in range(len(self.examples)):
            sample = self.examples[i]
            ht = self.labelTranslate(getResult(self.c[t],sample))
            yi = self.labelTranslate(sample[len(sample)-1])
            sum += yi * ht
        return 0.5 - 0.5*sum

    """
        creates bag of Decision tree
    """
    def bagwork(self):
        self.c = []
        for t in range(self.T):
            examplest = []
            i = math.floor(random.uniform(0,len(self.examples)))
            examplest.append(self.examples[i])
            tree = self.treemake(examplest)
            self.c.append(tree)
        self.a = self.votePredictions()


    """
        calculates vote Prediction from bag of classifier
    """
    def votePredictions(self):
        a = []
        for t in range(self.T):
            err = self.error(t)
            a.append((1-err)/err)
        return a



    """
        creates a full tree using ID3
    """
    def treemake(self,samples):
        attributes = self.description["attributes"]
        columns = self.description["columns"]
        labels = self.description["label values"]
        label = MostCommonLabel(samples,columns,labels)
        attributes = solveNumberic(samples,attributes,columns)
    
        tree = ID3work(samples,label,attributes,columns,labels,entropy,-1,True)
        return ID3Tree(tree, columns,attributes)
