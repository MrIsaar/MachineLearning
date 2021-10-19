def createArray(size,zero=False,transposed = False):
    arr = []
    if transposed:
        for i in range(0,size):
            arrinner = []
            for j in range(0,size):
                if zero:
                    arrinner.append(0)
                else:
                    arrinner.append(j + i+1)
            arr.append(arrinner) 
        return arr
    for i in range(0,size):
        arrinner = []
        for j in range(0,size):
            if zero:
                arrinner.append(0)
            else:
                arrinner.append(j + i+1)
        arr.append(arrinner) 
    return arr

def loop(size=512):
    
    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)

    for i in range(0,size):
        for j in range(0,size):
            for k in range(i,size): #i = val,k occurs val  0,1 1,2 2,3
                c[i][j] += a[i][k]*b[k][j]
    return c
def loop(size=512):
    
    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)

    for i in range(0,size):
        for j in range(0,size):
            for k in range(j,size): #i = val,k occurs val  0,1 1,2 2,3
                c[i][j] += a[i][k]*b[k][j]
    return c

def loopmid(size=512):
    
    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)

    for i in range(0,size):
        for k in range(i,size):
            for j in range(0,size):
             #i = val,k occurs val  0,1 1,2 2,3
                c[i][j] += a[i][k]*b[k][j]
    return c

def loopmod(size = 512):

    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)

    for k in range(0,size): # k = 0 -> i = [0,size] and j = [0,size]
        for i in range(0,k+1):
            for j in range(0,size):
                c[i][j] += a[i][k]*b[k][j]
    return c

def looppermk(size=512):
    
    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)

    for i in range(0,size):
        for j in range(0,size):
            rem = (size - j) % 3
            for k in range (j,j+rem):
                c[i][j] += a[i][k]*b[k][j]
            for k in range(j+rem,size,3): #i = val,k occurs val  0,1 1,2 2,3
                c[i][j] += a[i][k]*b[k][j] + a[i][k+1]*b[k+1][j] + a[i][k+2]*b[k+2][j]
    return c
def looppermj(size=512):
    
    a = createArray(size)
    b = createArray(size,transposed=True)
    c = createArray(size,True)
    message = ""

    for i in range(0,size):
        for j in range(0,size,3):
            """rem = (size - j) % 3
            for k in range(j,j+rem):
                c[i][j] += a[i][k]*b[k][j]"""
            for k in range(j,size-2):
                
                c[i][j] += a[i][k]*b[k][j]
                if k+1 < size:
                    c[i][j+1] += a[i][k+1]*b[k+1][j+1]
                else:
                    message +=  str(j+1) + "," + str(k+1) + " "
                    pass
                if k+2 < size :
                    c[i][j+2] += a[i][k+2]*b[k+2][j+2] 
                else:
                    message +=  str(j+2) + "," + str(k+2) + " "
                    pass
            
            k += 1
            c[i][j] += a[i][k]*b[k][j]    
            c[i][j + 1] += a[i][k+1]*b[k+1][j + 1]
            k += 1
            c[i][j] += a[i][k]*b[k][j]
            
            
            
    return c

size = 2*3
tested = looppermj(size)
ijk = loop(size)

errors = ""
for i in range(0,size):
    prob = False
    for j in range(0,size):
        if (ijk[i][j] != tested[i][j]):
                prob = True
    if prob:
        errors += "(" + str(i)  + ") "
print (errors)

