import numpy as np
from proccessFiles import processCSV
import random as r
import scipy
import scipy.optimize
import math
BIAS_X = 1
def splitExamples(examples):
    x = []
    y = []
    for i in range(len( examples)):
        xterm = examples[i][:-1]
        xterm.append(BIAS_X)
        x.append(xterm)
        
        y.append(examples[i][-1:][0])
    x = np.array(x)
    y = np.array(y)
    return (x,y)

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
            
        self.x, self.y = splitExamples(self.examples)
        

        self.w = np.zeros(len(self.examples[0]))
        #len(self.examples[0])-1
        #self.bias = self.w[-1:]
        if learningtype == "sgd":
            self.sgdSVM()
        if learningtype == "dual":
            self.alpha = np.zeros(len(self.examples))
            self.dualSVM()

    def prediction(self,sample):
        xi = sample[:-1]
        xi.append(BIAS_X) #bias value
        return np.dot(self.w,xi)  #+ self.bias

    def updateWeight(self,example,t):
        xi = example[:-1]
        xi.append(BIAS_X) #bias value
        yi = example[-1:]
        xy = np.multiply(xi,yi)
        rc = self.learningRate(t)*self.C
        update = self.learningRate(t)*(xy + np.multiply(-2*(1/t),self.w))

        self.w = self.w + update
        
        
        
    
    def sgdSVM(self):
        for t in range(1,self.t):
            r.shuffle(self.examples)
            wrongguess = False
            for i in range(len(self.examples)):
                pred = self.prediction(self.examples[i])
                error = self.examples[i][len(self.examples[i])-1] * pred
                if error <= 1:
                    self.updateWeight(self.examples[i],t)
                    wrongguess = True
                else: 
                    self.w = np.multiply(self.w,(1-self.learningRate(t)))
            if ( not wrongguess) :
                break
            
        
        #self.bias = self.bias + np.multiply(example[-1:],rc)
        #previous
        #for j in range(len(self.w)):
        #    xy = np.multiply(example[j],example[-1:])
        #    self.w[j] = (1 - self.learningRate(t))*self.w[j] + xy*rc
        #self.bias = (1 - self.learningRate(t))*self.bias + example[-1:][0]*rc
        
        return self.w




    def wstar(self):
        """calculate wstar from alpha star and examples
        """
        wstar = np.zeros(len(self.x[0][:-1]))
        for i in range(len(self.x)):
            calc = np.multiply(self.x[i][:-1],self.y[i]*self.alpha[i])
            wstar += calc
        j = math.floor(r.uniform(0,len(self.x)))
        wstar = np.concatenate((wstar,[0]))
        bias = self.y[j] - np.dot(self.x[j],wstar)
        wstar[len(wstar)-1] = bias
        return wstar
    
    def objective(self,alpha,x,y):
        """objective function for dual SVM 
          (1/2) sum(i){sum(j){  yiyj aiaj xi^Txj}} - sum(i){ai}
          
          s.t. 0<ai<C , sum(i){aiyi} == 0
          pg 96 Nonlinear SVM
        """
        #y = self.y
        #x = self.x
        
        alpha = alpha
        sum = 0
        
        """substitute for matrix and vector operations"""
        for i in range(len(x)):
            for j in range(len(x)):
                sum += y[i]*y[j]*alpha[i]*alpha[j]*np.inner(x[i],x[j])
        sum /= 2
        for i in range(len(x)):
            sum -= alpha[i]
        return sum
    
    def dualSVM(self):
        setting = "mehtod=SLSOP"
        MyBounds = [(0,self.C) for a in self.alpha] # 0 <= alpha <= C
        self.constraint = lambda alpha : np.dot(alpha,self.y)
        MyConstraints = ({'type':'eq','fun':self.constraint})# sum(i){ aiyi } = 0 
        result = scipy.optimize.minimize(self.objective,self.alpha,args=(self.x,self.y),method="SLSQP",bounds=MyBounds,constraints=MyConstraints)
        self.alpha = result.x
        if(not result.success):
            print("somthing went wrong with the dual SVM:\n ",result.message)
        #print(self.constraint(self.alpha))
        self.w = self.wstar()


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

    