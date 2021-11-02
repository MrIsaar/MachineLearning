import math
import random
from proccessFiles import processCSV
class perceptron():
    def __init__(self,examples,T,r,updateOn="standard"):
        """
            Given a set of examples (xi,yi) builds a linear classifier
            T epochs, r learning rate
            updateOn specifies how perceptron updates:
                standard, voted, and average.
                if updateOn is given a fuction it will be used.
                function must be of form (w,xi,yi,r) and decide underwhat
                conditions the update occurs
        """
        

        self.examples = examples
        if(type(examples) is str):
            self.examples = processCSV(examples)

        self.w = [0 for i in range(len(self.examples[0])-1)]
        self.bias = 0
        self.T = T
        self.r = r
        self.updateOn = updateOn
        self.updateDecide()
        self.perceptronwork()

    def perceptronwork(self):
        for t in range(self.T):
            
            #random.shuffle(self.examples)
            shuffle = self.examples
            for i in range(len(shuffle)):
                yi = shuffle[i][len(shuffle[i])-1]
                xi = shuffle[i][:-1]
                
                
                self.w = self.updatefunc(w=self.w,xi=xi, yi=yi,r=self.r,bias=self.bias)
        return

    

    def updateDecide(self):
        if type(self.updateOn) is str:
            if self.updateOn == "standard":
                self.updatefunc = lambda w,xi,yi,r,bias : self.updateStandard(w,xi,yi,r,bias)
            if self.updateOn == "voted":
                self.updatefunc = lambda w,xi,yi,r,bias : self.updateVoted(w,xi,yi,r,bias)
                self.m = 0#[0 for i in range(len(self.examples[0])-1)]
                self.c = [1]
                self.w = [self.w]
                self.bias = [self.bias]
            if self.updateOn == "average":
                self.updatefunc = lambda w,xi,yi,r,bias : self.updateAverage(w,xi,yi,r,bias)
        else:
            self.updatefunc = self.updateOn
        


    def updateStandard(self,w,xi,yi,r,bias):

        #predict
        wx = 0 
        for j in range(len(xi)):
            wx += w[j] * xi[j] 
        wx += bias
        sample = xi.copy()
        sample.append(yi)
        wx = self.prediction(sample)

        #update
        if yi * wx <= 0 or True:
            
            error = yi - wx
            for j in range(len(w)):
                #w[j] +=  r*yi*xi[j]
                w[j] +=  r*error*xi[j]

            #bias
            #bias += r*yi*1
            bias += r*error
            self.bias =bias
        else:
            pass
        return w
        

    def updateVoted(self,w,xi,yi,r,bias):
        wx = 0 
         
        for j in range(len(xi)):
            wx += w[self.m][j] * xi[j] 
        wx += w[self.m][len(w[self.m])-1] * 1
        if yi * wx <= 0:
            wj = []
            
            for j in range(len(w[self.m])-1):
                wj.append(w[self.m][j] + r*yi*xi[j])
            bias.append( bias[self.m] + r*yi*1)

            self.m = self.m+1
            w.append(wj)
            self.c.append(1)
        else:
            self.c[self.m]+= 1
        self.bias = bias
        return w


    def updateAverage(w,xi,yi,r):
        raise Exception("not implemented")
    
        
        
    def prediction(self,sample):
        xi = sample[:len(self.w)]
        wx=0
        for j in range(len(xi)):
            wx += (self.w[j] * xi[j] )
        wx += self.bias
        if wx >= 0.0:
            return 1.0
        return 0.0
        #
        # return wx/abs(wx)




    def votedPrediction(self,sample):
        xi = sample[:len(self.w)-1]
        sum = 0
        for i in range(len(self.w)):
            if i == 0:
                i = 1
            wx=0
            for j in range(len(xi)):
                wx += (self.w[i][j] * xi[j] )
            try:
                pred = wx/abs(wx)
            except ZeroDivisionError:
                pred=1
            sum = self.c[i] * pred
        return sum/abs(sum)

        



if __name__ == "__main__":
    #examples = [[i+1,i+10,(-1)**i] for i in range(5)]
    examples = [[1,1,1],[1,-1,1],[-1,1,-1],[-1,-1,-1]]
    percept = perceptron(examples,6,0.1)
    count = 0
    total = 0
    for example in examples:
        pred = percept.prediction(example)
        if example[-1:][0] == pred:
            count +=1
        total +=1
    print("correct standard: ",str(count),"/",str(total))

    percept = perceptron(examples,6,0.1,updateOn="voted")
    count = 0
    total = 0
    for example in examples:
        pred = percept.votedPrediction(example)
        if example[-1:][0] == pred:
            count +=1
        total +=1
    print("correct voted: ",str(count),"/",str(total))
