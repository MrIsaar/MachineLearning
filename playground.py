import math
def entropy(labelDict,itemsSeen):
    entropyVal = 0.0
    for label in labelDict:
        p = labelDict[label]/itemsSeen
        if not p:
            continue
        curr = p * math.log(p,2)
        entropyVal += curr
        
    return -entropyVal

amount = 3
"(5+(5/14)"
ent = entropy({"+":2,"-":1},amount)


print(str(ent)[:5])
print(0.918-0-0-(2/3)*1)
