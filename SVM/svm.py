import numpy as np
from proccessFiles import processCSV
import random as r
class svm(object):
    def __init__(self, examples, t, learningrate,learninga,C,learningtype="sgd"):
        self.C = C
        self.r = learningrate
        self.a = learninga
        self.t = t
        self.learningRate = lambda t : self.r/(1+(self.r/self.a)*t)
        self.examples = examples
        if(type(examples) is str):
            self.examples = processCSV(examples)

        self.w = np.zeros(len(self.examples[0])-1)
        #len(self.examples[0])-1
        self.bias = 0
        if learningtype == "sgd":
            self.sgdSVM()

    def prediction(self,sample):
        xi = sample[:-1]
        
        return np.dot(self.w,xi) + self.bias

    def updateWeight(self,example,t,error):
        rc = self.learningRate(t)*self.C
        #testing  w ← w − �t [w0; 0] + �t C N yi xi
        xy = np.multiply(example[:-1],example[-1:])
        self.w = self.w - self.learningRate(t)* self.w + xy*rc
        self.bias = self.bias + np.multiply(example[-1:],rc)
        #previous
        #for j in range(len(self.w)):
        #    xy = np.multiply(example[j],example[-1:])
        #    self.w[j] = (1 - self.learningRate(t))*self.w[j] + xy*rc
        #self.bias = (1 - self.learningRate(t))*self.bias + example[-1:][0]*rc
        
        return self.w

    def sgdSVM(self):
        for t in range(self.t):
            r.shuffle(self.examples)
            wrongguess = False
            for i in range(len(self.examples)):
                pred = self.prediction(self.examples[i])
                error = self.examples[i][len(self.examples[i])-1] * pred
                if error <= 1:
                    self.updateWeight(self.examples[i],t,error)
                    wrongguess = True
                else: 
                    self.w = np.multiply(self.w,(1-self.learningRate(t)))
            if ( not wrongguess) :
                break



if __name__ == "__main__":
    examples = [[2,2,1],[2,-2,1],[-2,2,-1],[-2,-2,-1]]
    
    c = [(100/873),(500/873),(700/873)]
    Svm = svm(examples,10,0.1,2,c[0],"sgd")

    count = 0
    total = 0
    for example in examples:
        pred = Svm.prediction(example)
        if example[-1:][0] * pred >= 0:
            count +=1
        total +=1
    print("correct spliting: ",str(count),"/",str(total))

    examples = [[1,2,1],[0,3,1],[2,3,-1],[2,4,-1]]
    
    
    Svm = svm(examples,10,0.1,2,c[0],"sgd")

    count = 0
    total = 0
    for example in examples:
        pred = Svm.prediction(example)
        if example[-1:][0] * pred >= 0:
            count +=1
        total +=1
    print("correct bais test: ",str(count),"/",str(total))

    