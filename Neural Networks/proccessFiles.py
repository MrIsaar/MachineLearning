"""
    used for processing a CSV file where each item is seperated with a newline
    and each attribute is comma seperated (',')
    i.e. 
    low,vhigh,4,4,big,med,acc
    low,high,5more,4,med,high,vgood

    debugprint will print the first debugprint number of elements in file. default is 0
"""
def processCSV(CSVfile, debugprint=0):
    
    index = 0
    items = []
    with open(CSVfile) as f:
        for line in f:
            terms = line.strip().split(',')
            for i in range(len(terms)):
                terms[i] = float(terms[i])
            if(terms[len(terms)-1] == 0):
                terms[len(terms)-1] = -1
            items.append(terms)
            if debugprint > index:
                print(items[index])
            index += 1
    return items