import sys
sys.path.insert(0, '../part2')
import tbl
import math
import random
import statistics

# return a list of random numbers 
# the size of the list = count, range for numbers = [min, max]
random.seed(5)
def randomNumRange(count, min, max):
    numList = []
    for x in range(0, count):
        numList.append(random.uniform(min, max))
    return numList

def ranges(table, colIndex):
    values = []
    for r in table.rows:
        row = table.rows[r]
        value = row.cells[colIndex]
        if value is not None:
            values.append(value)

    col = table.cols["all"][colIndex]
    make_bins(values, col.sd)

# May be in our case we can create column data list
def make_bins(numList, sd):
    numList.sort()
    print("\n " + str(numList))
    n = len(numList)
    minBinSize = round(math.sqrt(n))
    espilon = 0.2*statistics.stdev(numList)
    numInitBins = math.floor(n/minBinSize) #total number of initial bins
   
    print(str(numInitBins) + " Num of Bins\n" + str(minBinSize) +  "min bin size\n")

    # Had issues trying to initialize a dictionary key value dynamically.
    # for now, calculated the number of keys before
    prop = ['span', 'low', 'n', 'high']
    ranges_dic = {}
    for i in range(1, numInitBins+1):
        ranges_dic[i] = {}
    for i in range(1, numInitBins+1):
        for p in prop:
            ranges_dic[i][p] = '0'
    
    jump_size = 0
    #initialize bins
    for i in range(1, numInitBins+1):
        try:
            start = jump_size
            end = jump_size + minBinSize -1
            ranges_dic[i]['low'] = numList[start]
            ranges_dic[i]['high'] = numList[end]
            ranges_dic[i]['span'] = ranges_dic[i]['high'] - ranges_dic[i]['low']
            ranges_dic[i]['n'] = minBinSize
            # in case there are fewer elements than minBinsSize at the end
            # add it to the last bin
            if(i == numInitBins and end < n -1):
                ranges_dic[i]['high'] = numList[n-1]
                ranges_dic[i]['span'] = ranges_dic[i]['high'] - ranges_dic[i]['low']
                ranges_dic[i]['n'] = minBinSize + ((n-1)-end)
            jump_size = jump_size + minBinSize
        except:
            print("something is going wrong")

    printDictionary(ranges_dic)
        
    #At this point - (1) is met, need to check 
        #(1) >=minBinsize
        #(2) ranges differ by epsilon
        #(3) span of range > epsilon
        #(4) low is greater than hi of prev range
        
    pass

#print the dictionary
def printDictionary(dictt):
    for keys,values in dictt.items():
        print(keys)
        print(values)
    return
    
    
def super_ranges(table, colIndex):
    pass

table = tbl.Tbl();
table.update({0:"$someNumeric"})
randomValues = randomNumRange(10,1, 23)
for val in randomValues:
    table.update({0:val})


ranges(table, 0)

for i, col in table.cols["all"].items():
    col.summarize()

