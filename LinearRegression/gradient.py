from proccessFiles import processCSV
import proccessFiles
import math

def strtofloat(samples):
    for i in range(len(samples)):
        num = [float(strn) for strn in samples[i] ]
        samples[i] = num
    return samples

def calcGradent(samples,w):
    if len(samples[0])-1 != len(w):
        raise Exception("len of sample != len of w")
    dw = []
    for j in range(len(w)):
        sum = gradientItem(samples,w,j)
        dw.append(-sum)
    
    return dw

def gradientItem(samples,w,j):
        sum = 0
        for i in range(len(samples)):
            wx = 0
            for l in range(len(samples[i])-1):
                wx += (w[l]*float(samples[i][l]))
            #wx += w[l+1] # bias
            # yi - wTxi xij
            err = (samples[i][len(samples[i])-1]- wx)
            sum += (err*samples[i][j])
        return sum

class gradent():
    def __init__(self,CSV,errorTolerance,learningRate) -> None:
        self.samples = processCSV(CSV)
        self.samples = strtofloat(self.samples)
        self.w = [0 for i in range(len(self.samples[0])-1)]
        
        self.r = learningRate
        self.e = errorTolerance

        self.descent()

    def descent(self):
        
        self.costs = [0 for k in range(3)]
        min = 0
        while self.e < self.cost():
            self.costs[min]=(self.cost())
            dJ = calcGradent(self.samples,self.w)
            wnext = [(self.w[i] - self.r* (dJ[i]/abs(dJ[i]))) for i in range(len(self.w))]
            #for i in range(len(self.w)):
                #wnext[i] = (self.w[i] - self.r* dJ[i])
            
            self.w = wnext
            
            if(min == 2 and self.costs[0] - self.costs[2] < 0.51 ):
                self.bias = (self.costs[2])
                return self.w
            min += 1
            min = min % 3
        return self.w

    # 0.3, 0.6, 0.9
    
    def cost(self):
        
        sum = 0
        for i in range(len(self.samples)):
            wx = 0
            for l in range(len(self.samples[i])-1):
                wx += (self.w[l]*float(self.samples[i][l]))
            #wx += self.w[l+1] # bias
            sum += ((float(self.samples[i][len(self.samples[i])-1])- wx))**2
        
        
        cost = 0.5 *sum
        return cost

    def result(self,sample):
        wx = 0
        for l in range(len(sample)-1):
            wx += (self.w[l]*sample[l])
        return wx + self.bias

