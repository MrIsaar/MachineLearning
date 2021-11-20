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
    
    def __init__(self, examples, t, learningrate,learninga,C,learningtype="sgd",kernalTrue = False):
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
            self.kernalTrue = kernalTrue
            self.dualSVM()
        if learningtype == "kernal":
            self.alpha = np.zeros(len(self.examples))
            self.kernalTrue = True
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
        w0 = self.w[:-1]
        w0 = np.concatenate((w0,[0]))
        #update = self.learningRate(t)*(xy + np.multiply(-2*(1/t),self.w))
        update = -self.learningRate(t)*w0 + self.learningRate(t)*self.C*len(self.examples)*np.multiply(xi,yi)
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
                    w0 = self.w[:-1]
                    
                    w0 = np.multiply(w0,(1-self.learningRate(t)))
                    self.w = np.concatenate((w0,self.w[-1:]))
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
            w* = sum(i) {aiyixi}
        """
        wstar = np.zeros(len(self.x[0][:-1]))
        for i in range(len(self.x)):
            calc = np.multiply(self.x[i][:-1],self.y[i]*self.alpha[i])
            wstar += calc
            
        """"
            calculate bias
            b* = (1/#notzero alpha) sum(notzero alpha) (yi - wTxi)
        """
        bias = 0
        count = 0
        for i in range(len(self.x)):
            if(self.alpha[i] > 0.0001):
                bias += (self.y[i] - np.dot(wstar,self.x[i][:-1]))
                count += 1
        bias = (1/count)*bias
        
        wstar = np.concatenate((wstar,[bias]))
        """    
        j = math.floor(r.uniform(0,len(self.x)))
        wstar = np.concatenate((wstar,[0]))
        bias = self.y[j] - np.dot(self.x[j],wstar)
        wstar[len(wstar)-1] = bias"""
        return wstar
    
    def objective(self,alpha,x,y,kernal):
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
        """
        for i in range(len(x)):
            for j in range(len(x)):
                sum += y[i]*y[j]*alpha[i]*alpha[j]*np.inner(x[i],x[j])
        """
        o = (((alpha*y*np.ones((len(y),len(y)))).T)*alpha*y)
        val = []
        if(not kernal):    
            val = np.matmul(x,x.T) # xs = val
        else:
            for i in range(len(x)):
                valin = []
                for j in range(len(x)):
                    valin.append(self.kernal(x[i],x[j]))
                val.append(valin)
            val = np.array(val)
        sum = np.dot(o.flatten(),val.flatten())
        sum /= 2
        val = alpha.sum()
        """
        for i in range(len(x)):
            val += alpha[i]
        """
        
        sum -= val
        return sum
    
    def dualSVM(self):
        setting = "mehtod=SLSQP"
        MyBounds = [(0,self.C) for a in self.alpha] # 0 <= alpha <= C
        self.constraint = lambda alpha : np.dot(alpha,self.y)
        MyConstraints = ({'type':'eq','fun':self.constraint})# sum(i){ aiyi } = 0 
        result = scipy.optimize.minimize(self.objective,self.alpha,args=(self.x,self.y,self.kernalTrue),method="SLSQP",bounds=MyBounds,constraints=MyConstraints)
        self.alpha = result.x
        if(not result.success):
            print("somthing went wrong with the dual SVM:\n ",result.message)
        #print(self.constraint(self.alpha))
        self.w = self.wstar()
        
    def kernal(self,xi,xj):
        mag = 0
        c = 0
        for i in range(len(xi)):
            mag += (xi[i] - xj[i])**2
            c += 1
        upper = mag
        """
        mag= mag **(1/2)
        upper = (xi - xj)/mag
        if(mag == 0):
            upper = np.zeros(upper.shape)
        else:
            upper = upper*upper
        """
        
        return np.exp(-(upper/self.r))
        
        
        


if __name__ == "__main__":
    examples = [[2,2,1],[2,-2,1],[-2,2,-1],[-2,-2,-1]]
    
    c = [(100/873),(500/873),(700/873)]
    Svm = svm(examples,10,0.1,2,c[0],"sgd")
    kernal = Svm.kernal(Svm.x[2][:-1],Svm.x[0][:-1])
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

    