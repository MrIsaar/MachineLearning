"""
tset is a training set (x1,y1) to (xm,ym)
xi exists in X
yi exists in {-1,+1}
T is depth of learning
"""
import math
import ID3Constructor
from proccessFiles import proccesDesc, processCSV
from ID3Constructor import ID3setup,solveNumberic,MostCommonLabel
from ID3 import getResult,ID3



def normalized(d):
        sum = 0
        err = 0.01
        for di in d:
            sum += di
        if sum >= (1 - err) and sum <= (1 + err):
            return True
        return False
def normalize(d):
    sum = 0
    for di in d:
        sum += di
    
    i = 0
    for di in d:
        d[i] = di/sum
        i+=1
    return d

def weightedentropy(examples,labels,columns):
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
   

class AdaBoost: 
    

    def labelTranslate(self,label):
        if type(label) is not str:
            return label
        if(label == self.labels[0]):
            return -1
        if(label == self.labels[1]):
            return 1
    #ensure if not yes/no it is a number
    

    def weightedentropy(self,examples,labels,columns):
        if(len(examples) <= 1):
            return 0.0
    
        LIndex = columns.index("label")
        itemsSeen = 0
        entropyVal = 0
        labelDict = {}
        i = 0
        for example in examples:
            currlabel = example[LIndex]
            if not labels.__contains__(currlabel):
                raise Exception("label not in label list: " + currlabel)
            if not labelDict.__contains__(currlabel):
                labelDict[currlabel] = 0
            labelDict[currlabel] += 1
            itemsSeen += 1
            
        if itemsSeen != len(examples):
         #   raise Exception("entropy not same count something is wrong")
            pass

        
        for label in labelDict:
            
            p = (labelDict[label]/itemsSeen) * (1/self.d[i])
            curr = p * math.log(p,2)
            entropyVal += curr
            i+=1
            
        
        return -entropyVal
    
        
    """
    pg 32
    """
    def error(self,t):
        sum = 0
        for i in range(len(self.examples)):
            sample = self.examples[i]
            ht = self.labelTranslate(getResult(self.h[t],sample))
            yi = self.labelTranslate(sample[len(sample)-1])
            sum += self.d[i] * yi * ht
        return 0.5 - 0.5*sum
    
    
    def AdaBoostWork(self,T):
        d = []
        a   = []
        self.h = []
        m = len(self.examples)
        for i in range(m):
            d.append(1/m)
    
        for t in range(T):
            dt = d.copy()
            self.d = d
            ht = ID3(self.csv,self.dataDesc,1,self.weightedentropy,True)
            self.h.append(ht) 
             #weighted classification error better than chance, naive linear classifer
            err = self.error(t)
            a.append( 0.5*math.log((1-err)/err))
            
            for i in range(m) :
                xi = self.examples[i].copy()
                
                yi = xi[len(xi)-1]
                yi = self.labelTranslate(yi)
                hi = self.labelTranslate(getResult(ht,xi))
                d[i] = (dt[i])*math.exp(-a[t]*yi*hi) 
                
            normalize(d)
            

        #final hypothesis
        self.a = a
        
        self.T = T
        self.implemented = True

        return self
        
    
    def Hfinal(self,sample):
            
            sign = 0
            for t in range(self.T):  
                hi = self.labelTranslate(getResult(self.h[t],sample))
                sign += self.a[t]*hi
            if(sign < 0):
                #negative option
                return self.labels[0]
            if(sign > 0):
                #positive option
                return self.labels[1]
            return 0

    def __init__(self,CSVfile,dataDescFile):
        self.description = proccesDesc(dataDescFile)
        
        self.examples = processCSV(CSVfile)
        self.csv = CSVfile
        self.dataDesc = dataDescFile
        #self.attributes = self.description["attributes"]
        #self.columns = self.description["columns"]
        self.labels = self.description["label values"]
        #self.label = MostCommonLabel(self.examples,self.columns,self.labels)
        #self.attributes = solveNumberic(self.examples,self.attributes,self.columns)
    
        #self.tree = ID3(CSVfile,dataDescFile,maxdepth=2,handleUnknown=True)
        return self.AdaBoostWork(T)  


