
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

            items.append(terms)
            if debugprint > index:
                print(items[index])
            index += 1
    return items


"""
    processes description file into a dictonary
    must be in the form where each key is preceded by a '|' character and lists of values must be comma ',' seperated.
    attributes key will create value as a dictionary with value preceding a ':' is the key and the after part is assumed
    to be a list
    
    example file is 
| label values
unacc, acc, good, vgood
| attributes
buying:   vhigh, high, med, low.
maint:    vhigh, high, med, low.
doors:    2, 3, 4, 5more.
persons:  2, 4, more.
lug_boot: small, med, big.
safety:   low, med, high.
| columns
buying,maint,doors,persons,lug_boot,safety,label

"""
def proccesDesc(dataDescFile,debugprint=False):
    values = {}
    
    with open(dataDescFile) as f:
        value=""
        terms={}
        for line in f:
            if len(line.strip()) == 0:
                continue
            if line.strip().startswith('|'):
                if(len(terms) > 0):
                    values[value] = terms
                value = line.split('|')[1].strip()
                continue
            else:
                if(value == "attributes"):
                    attributeline = line.strip().split(':')
                    attribute = attributeline[0].strip()
                    terms[attribute] = attributeline[1].strip().split(',')
                    for i in range(len(terms[attribute])):
                        temp = terms[attribute][i].strip()
                        if(temp.endswith('.')):
                            temp = temp[:len(temp)-1]
                        terms[attribute][i] = temp
                else:
                    split = line.strip().split(',')
                    for i in range(len(split)):
                        split[i] = split[i].strip()
                    values[value] = split
                        
    if(debugprint):
        for value in values:
            print(value + ":")
            output = ""
            for v in values[value]:
                
                if value == "attributes":
                    output = "        " + v + " : ["
                    for attribute in values[value][v]:
                        output += attribute + ", "
                    print(output[:len(output)-2] + "]")
                else:
                    output += v + ", "
            if value != "attributes":
                print("        " + output[:len(output)-2] + "\n")
            else:
                print("") # newline
    return values



