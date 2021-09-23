import math
"""
    calculates entropy 
    - sum ( plog2(p)  )
"""
def entropy(examples,labels,columns):
    if(len(examples) <= 1):
        return 0.0
    
    LIndex = columns.index("label")
    itemsSeen = 0
    entropyVal = 0
    labelDict = {}
    for example in examples:
        currlabel = example[LIndex]
        if not labels.__contains__(currlabel):
            raise Exception("label not in label list: " + currlabel)
        if not labelDict.__contains__(currlabel):
            labelDict[currlabel] = 0
        labelDict[currlabel] += 1
        itemsSeen += 1
    if itemsSeen != len(examples):
        raise Exception("entropy not same count something is wrong")
    for label in labelDict:
        p = labelDict[label]/itemsSeen
        curr = -1 * p * math.log(p,2)
        entropyVal += curr
        
    return entropyVal

    #e1= entropy(posp,pos)
    #e2= entropy(negp,neg)
    #e = e1 * (pos/total) + e2 * (neg/total) 
    return 0.0

def tempEntropy(_pos,_total):
    plus=_pos/_total
    minus=(_total-_pos)/_total
    
    #print("p+: " + str(-(plus*math.log(plus,2))) + ", p-: " + str((-minus*math.log(minus,2))) )
    if(plus == 0):
        return (minus*math.log(minus,2))
    if(minus == 0):
        return (plus*math.log(plus,2))
    return -(plus*math.log(plus,2)) - (minus*math.log(minus,2))

if __name__ == '__main__':
    from ID3Constructor import ID3setup
    import os
    #CSVfile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/train.csv"
    #dataDescFile = "C:/Users/Isaac Gibson/source/VS code/a01/MachineLearning/car/data-desc.txt"

    print (__file__)
    dirname = os.path.dirname(os.path.dirname(__file__))
    print(dirname)
    filename = dirname + '/car/train.csv'
    print(filename)
    descriptFile = dirname + "/car/data-desc.txt"
    tree = ID3setup(filename,descriptFile,entropy)
    print("done")