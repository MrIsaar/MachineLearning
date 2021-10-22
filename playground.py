def cost (y,w,x,b):
    if(len(y) != len(x)):
        raise Exception()
    sum = 0
    for i in range(0,len(y)):
        suminner = 0
        if(len(x[i]) != len(w)):
                raise Exception()
        for j in range (0,len(w)):
            suminner += (x[i][j] * w[j])
        suminner = (y[i] - suminner)**2
        sum += suminner
    sum = sum/2
    return sum + b/2

y=[1,4,-1,-2,0]
w=[0.3,0.6,0.9]
x=[[1,-1,2],[1,1,3],[-1,1,0],[1,2,-4],[3,-1,-1]]
b = 1

c = cost(y,w,x,b)
print(c)

