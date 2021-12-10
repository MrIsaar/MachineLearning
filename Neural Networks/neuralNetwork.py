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
        xterm.insert(0,BIAS_X)
        
        x.append(xterm)
        
        y.append(examples[i][-1:][0])
    x = np.array(x)
    y = np.array(y)
    return (x,y)

def sigmoid(x):
    return 1/(1+math.exp(-x))

def correctWeights(w):
    top = np.zeros((3,4))
    mid = np.concatenate((np.zeros((1,3)),np.ones((3,3)))).T
    bottom = np.concatenate(((np.zeros((1,3)),np.ones((1,3)),np.ones((1,3)),(np.zeros((1,3)))))).T
    full = np.array([top,mid,bottom])
    return np.transpose(w.T*full)


class NNet(object):
    def __init__(self,examples,epochs,learningrate,learningd,width=None,randomWeight=True,verbose=False):
        """Neural Network that uses 1 input 2 hidden and 1 output layer
            weights are stored as 3d array
            w[layer][from][to]

        Args:
            examples (list or filepath): accepts form x,y where the last element of the list is the label
            epochs (int): specified epochs to run
            width (int): size hidden layers span (not including bias nodes). Defaults to size of example
            weight (str, optional): initalizes weight to random gaussian value or zero if false . Defaults to True.
        """
        
        
        self.r = learningrate
        self.a = learningd
        self.T = epochs
        self.learningRate = lambda t : self.r/(1+(self.r/self.a)*t)
        
        self.examples = examples
        if(type(examples) is str):
            self.examples = processCSV(examples)
        self.x, self.y = splitExamples(self.examples)
        
        
        if(width is None):
            self.width = len(self.x[0])
            width = self.width
        else:
            self.width = width + 1
        self.z = np.zeros((4,width))
        i = np.concatenate((np.ones((4,1)),np.zeros((4,width-1))),1) # init bias variables
        self.z = self.z+i
        
        
        if randomWeight:
            np.random.seed(12345)
            self.w = np.random.rand(4,width,width)
        else:
            self.w = np.zeros((4,width,width))
            
        self.dldz = np.zeros((4,width))
        self.dldw = np.zeros((4,width,width))
        
        self.sgdNeuralNet()
        
    
    def prediction(self,x):
        self.z[0] = x
       
        for layer in range(1,4):
            for toNode in range (1,len(self.w[layer][0])):
                
                for fromNode in range (0,3):

                    self.z[layer][toNode] += self.z[layer-1][fromNode]*self.w[layer][fromNode][toNode]
                if layer != 3:
                    self.z[layer][toNode] = sigmoid(self.z[layer][toNode])
        wt = self.w[3].T
        
        return np.dot(wt[1],self.z[2])
        
    
        
    def backPropFirst(self,x,label):
        """
        Implimentation of the Backpropigation algorithm
        
        """
        self.z[0] = x
        y = self.prediction(x) # initializes all z nodes and gets y
        "dldy =  y - y*" 
        dldy = y-label
        self.dldz[3][1] = dldy 
        
        
        "handle layer below output"
        layer = 3
        toNode = 1
        " dldw [3][i][1]"
        for fromNode in range(len(self.z[layer-1])):
            self.dldw[layer][fromNode][toNode] = dldy*(self.z[layer-1][fromNode])

        " dldz [2][i]"
        for fromNode in range(len(self.z[layer-1])):
            self.dldz[layer-1][fromNode] = dldy*(self.w[layer][fromNode][toNode])
            
        
        "general layers"
        for layer in range(2,0,-1):
            "find dldw"
            for fromNode in range(len(self.z[layer-1])):
                for toNode in range(1,len(self.w[layer][fromNode])):
                    self.dldw[layer][fromNode][toNode] = (self.dldz[layer][toNode])*(self.z[layer-1][fromNode])*self.z[layer][toNode]*(1-self.z[layer][toNode] )
                    
            "find dldz"
            for fromNode in range(len(self.z[layer-1])):
                dzdz = 0
                for toNode in range(1,len(self.w[layer][fromNode])):
                    dzdz += self.dldz[layer][toNode]* self.w[layer][fromNode][toNode] * self.z[layer][toNode]* (1-self.z[layer][toNode])
                self.dldz[layer-1][fromNode] =  dzdz
                
    def testBackProp(self):
        """
            tests back propigation by printing all dldw
            WARNING: replaces all weight vectors with the specified weights from the assignment
                    
        """
        self.w = np.array([[[0,0,0],[0,0,0],[0,0,0]],[[0,-1,1],[0,-2,2],[0,-3,3]],[[0,-1,1],[0,-2,2],[0,-3,3]],[[0,-1,0],[0,2,0],[0,-1.5,0]]])
        self.z = np.array([[1.0,1.0,1.0],[1.0,0.0,0.0],[1.0,0.0,0.0],[0.0,0.0,0.0]]) # inputs, layer1,layer2,output
        
       
        self.backPropFirst(1)
        print(self.dldw) #break point to check all values dl
        
    def sgdNeuralNet(self):
        for t in range(1,self.T):
            xyOrder = [i for i in range(len(self.x))]
            r.shuffle(xyOrder)
            for i in xyOrder:
                x = self.x[i]
                y = self.y[i]
                self.computeGradient(x,y) #computes loss
                self.updateWeights(t)
                
    def updateWeights(self,t):
        temp = self.w - self.learningRate(t)*self.dldw
        self.w = temp
        
    def computeGradient(self,x,label):
        y = self.prediction(x)
        h = 1
        for m in range(len(self.x)):
            for n in range(self.width):
                self.dldw[h][m][n] = self.backProp(h,m,n,y,label)
                
    def backProp(self,h,m,n,y,label):
        self.dldw[h][m][n] = 0
        if h+1 == 4:
            "dldy =  y - y*" 
            dldy = y-label
            self.dldz[3][1] = dldy
            return dldy*self.z[h-1][m]
        
        paths = np.array([])
        for toNode in range(1,len(self.w[h+1])):
            path = [(h+1,n,toNode)]
            for layer in range(h,len(self.w)-1):
                if h+1 == 4:
                    paths.append(path)
                
   
                
if __name__ == "__main__":
    nn = NNet([[1,1]],3)
    nn.testBackProp() # tests backpropigation