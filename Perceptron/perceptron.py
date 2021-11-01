import math
import random
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
        self.w = [0 for i in range(len(examples[0]))]
        
        self.examples = examples
        self.T = T
        self.r = r
        self.updateOn = updateOn
        self.updateDecide()
        self.perceptronwork()

    def perceptronwork(self):
        for t in range(self.T):
            random.shuffle(self.examples)
            shuffle = self.examples
            for i in range(len(shuffle)):
                yi = shuffle[i][len(shuffle[i])-1]
                xi = shuffle[i][:-1]
                
                
                self.w = self.updatefunc(w=self.w,xi=xi, yi=yi,r=self.r)
        return

    

    def updateDecide(self):
        if type(self.updateOn) is str:
            if self.updateOn == "standard":
                self.updatefunc = lambda w,xi,yi,r : self.updateStandard(w,xi,yi,r)
            if self.updateOn == "voted":
                self.updatefunc = lambda w,xi,yi,r : self.updateVoted(w,xi,yi,r)
                self.m = 0#[0 for i in range(len(self.examples[0])-1)]
                self.c = [1]
                self.w = [self.w]
            if self.updateOn == "average":
                self.updatefunc = lambda w,xi,yi,r : self.updateAverage(w,xi,yi,r)
        else:
            self.updatefunc = self.updateOn
        
    def updateStandard(self,w,xi,yi,r):
        wx = 0 
        for j in range(len(xi)):
            wx += w[j] * xi[j] 
        wx += w[len(w)-1] * 1
        if yi * wx <= 0:
            for j in range(len(w)-1):
                w[j] += w[j] + r*yi*xi[j]
            w[len(w)-1] += r*yi*1
        else:
            pass
        return w
        

    def updateVoted(self,w,xi,yi,r):
        wx = 0 
         
        for j in range(len(xi)):
            wx += w[self.m][j] * xi[j] 
        wx += w[self.m][len(w[self.m])-1] * 1
        if yi * wx <= 0:
            wj = []
            for j in range(len(w[self.m])-1):
                wj.append(w[self.m][j] + r*yi*xi[j])
            wj.append(w[self.m][len(w[self.m])-1] + r*yi*1)

            self.m = self.m+1
            w.append(wj)
            self.c.append(1)
        else:
            self.c[self.m]+= 1
        return w


    def updateAverage(w,xi,yi,r):
        raise Exception("not implemented")
    
        
        
    def prediction(self,sample):
        xi = sample[:len(self.w)-1]
        wx=0
        for j in range(len(xi)):
            wx += (self.w[j] * xi[j] )
        return wx/abs(wx)

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
