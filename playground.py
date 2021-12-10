import math
import random
import sys
import numpy as np

def dsig(x):
    """
    Derivitive of sigmoid sig(x)(1-sig(x))
    """
    return sigmoid(x)*(1-sigmoid(x))

def sigmoid(x):
    return 1/(1+math.exp(-x))




vals = []
w = np.array([[[0,0,0],[0,0,0],[0,0,0]],[[0,-1,1],[0,-2,2],[0,-3,3]],[[0,-1,1],[0,-2,2],[0,-3,3]],[[0,-1],[0,2],[0,-1.5]]])
z = np.array([[1.0,1.0,1.0],[1.0,0.0,0.0],[1.0,0.0,0.0],[0.0,0.0,0.0]])
x = np.array([1,1,1])

# z[1][1] += z[0][0] * w[1][0][1]
# z[1][1] += z[0][1] * w[1][1][1]
# z[1][1] += z[0][2] * w[1][2][1]

# print(z[1][1])
# z[1][1] = 0
for layer in range(1,4):
    for toNode in range (1,len(w[layer][0])):
        out = "z^"+str(layer)+"_"+ str(toNode) + " = \\sigma("
        for fromNode in range (0,3):
            if layer == 1:
                out += "x"
            else:
                out += "z"
            out += "^"+str(layer-1)+"_"+ str(fromNode) + "*w^"+ str(layer) + "_{" + str(fromNode) + " " + str(toNode) + "} + " 
            z[layer][toNode] += z[layer-1][fromNode]*w[layer][fromNode][toNode]
        if layer != 3:
            z[layer][toNode] = sigmoid(z[layer][toNode])
        out = out[:-2] + ") = " + str(z[layer][toNode])
        print(out)

dldz = np.zeros((3,3));
dldw = np.zeros((4,3,3));

wt = np.array([np.transpose(w[0]),np.transpose(w[1]),np.transpose(w[2]),np.transpose(w[3])])
#dldy = (w[3][0][1] + w[3][1][1] * z[2][1] + w[3][2][1] * z[2][2])-1
dldy = np.dot(wt[3][1],z[2])-1
layer = 3
toNode = 1
" dldw [3][i][1]"
for fromNode in range(len(z[layer-1])):
    dldw[layer][fromNode][toNode] = dldy*(z[layer-1][fromNode])
    print("\\frac{\partial L}{\partial w^{" + str(layer) + "}_{" + str(fromNode) +" "+ str(toNode) +"}} = ("+ str(dldy)[:6] +")(z^{"+ str(layer-1) +"}_{"+ str(toNode) +"} )= " + str(dldw[layer][fromNode][toNode])[:7] )

" dldz [2][i]"
for fromNode in range(len(z[layer-1])):
    dldz[layer-1][fromNode] = dldy*(w[layer][fromNode][toNode])
    print("\\frac{\partial L}{\partial z^{" + str(layer-1) + "}_{" + str(fromNode) +"}} = ("+ str(dldy)[:6] +")(w^{"+ str(layer) +"}_{"+ str(fromNode)+ str(toNode) +"} )= " + str(dldz[layer-1][fromNode])[:7] )
    
for layer in range(2,0,-1):
    "find dldw"
    for fromNode in range(len(z[layer-1])):
        for toNode in range(1,len(w[layer][fromNode])):
            
            dldw[layer][fromNode][toNode] = (dldz[layer][toNode])*(z[layer-1][fromNode])*z[layer][toNode]*(1-z[layer][toNode] )
            "check calc of which nodes to use"
            print("\\frac{\partial L}{\partial w^{" + str(layer) + "}_{" + str(fromNode) +" "+ str(toNode) +"}} = (\\frac{\partial L}{\partial z^{" + str(layer) + "}_{" + str(toNode) +"}})(z^{"+ str(layer-1) +"}_{"+ str(fromNode) +"} )" +"(z^{"+ str(layer) +"}_{"+ str(toNode) +"} )"+"(1 - z^{"+ str(layer) +"}_{"+ str(toNode) +"} )"+"=" + str(dldw[layer][fromNode][toNode])[:7] )
    "find dldz"
    for fromNode in range(len(z[layer-1])):
        dzdz = 0
        out = "\\frac{\partial L}{\partial z^{" + str(layer-1) + "}_{" + str(fromNode) +"}} =" 
        for toNode in range(1,len(w[layer][fromNode])):
            dzdz += dldz[layer][toNode]* w[layer][fromNode][toNode] * z[layer][toNode]* (1-z[layer][toNode])
            out += "\\frac{\partial L}{\partial z^{" + str(layer) + "}_{" + str(toNode) +"}} w^{" + str(layer) + "}_{" + str(fromNode) + " " + str(toNode) + "} " + "z^{" + str(layer) + "}_{" + str(toNode) + "} " + "(1-z^{" + str(layer) + "}_{" + str(toNode) + "} )+"
        dldz[layer-1][fromNode] =  dzdz
        print(out[:-1] + "= " + str(dldz[layer-1][fromNode])[:7])
        

print("testing")