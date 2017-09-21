import sys
sys.path.insert(0, '../part2')
import tbl
import math
import random
import statistics

################ Unsupervised Discretization #####################

def ranges(table, colIndex):
    values = get_values(table, colIndex)
    col = table.cols["all"][colIndex]
    sd = col.sd
    bins = make_bins(values, sd)
    printDictionary(bins)

# May be in our case we can create column data list
def make_bins(numList, sd):
    numList.sort()
    print("\n " + str(numList))
    n = len(numList)
    minBinSize = round(math.sqrt(n))
    espilon = 0.2*statistics.stdev(numList)
    numInitBins = math.floor(n/minBinSize) #total number of initial bins
   
    print(str(numInitBins) + " Num of Bins\n" + str(minBinSize) +  " Min bin size\n")

    # Had issues trying to initialize a dictionary key value dynamically.
    # for now, calculated the number of keys before
    prop = ['span', 'low', 'n', 'high']
    ranges_dic = {}
    for i in range(1, numInitBins+1):
        ranges_dic[i] = {}
    for i in range(1, numInitBins+1):
        for p in prop:
            ranges_dic[i][p] = '0'
    
    cur_pos = 0
    #initialize bins
    for i in range(1, numInitBins+1):
        try:
            start = cur_pos
            end = cur_pos + minBinSize -1
            ranges_dic[i]['low'] = numList[start]
            ranges_dic[i]['high'] = numList[end]
            ranges_dic[i]['span'] = ranges_dic[i]['high'] - ranges_dic[i]['low']
            ranges_dic[i]['n'] = minBinSize
            # in case there are fewer elements than minBinsSize at the end
            # add it to the last bin
            if(i == numInitBins and end < n-1):
                ranges_dic[i]['high'] = numList[n-1]
                ranges_dic[i]['span'] = ranges_dic[i]['high'] - ranges_dic[i]['low']
                ranges_dic[i]['n'] = minBinSize + ((n-1)-end)
            cur_pos = cur_pos + minBinSize
        except:
            print("something is going wrong")

          
    #At this point - (1) is met, need to check 
        #(1) >=minBinsize
        #(2) ranges differ by epsilon
        #(3) span of range > epsilon
        #(4) low is greater than hi of prev range
        
    printDictionary(ranges_dic)
    
    #At this point MET (1) >=minBinsize 
    last_key = numInitBins
    test_dict = ranges_dic.copy()
    traverseKeys = list(test_dict)
    for k in traverseKeys:
        if(test_dict[k]!= None):
            #last bins span is smaller - condition (3) edge case
            if(k == last_key and test_dict[k]['span']< espilon):
                mergeBins(test_dict, k-1, k)
            # span of bins is small - condition (3)
            elif(test_dict[k]['span']< espilon):
                mergeBins(test_dict, k, k+1)
    #condition (2) MET
    printDictionary(test_dict)

    #TODO (3) and (4) 
        
    return test_dict

################ Supervised Discretization #####################

def super_ranges(table, colIndex, depIndex):
    indep_values = get_values(table, colIndex)
    sd = table.cols["all"][colIndex].sd
    unsup_ranges = make_bins(indep_values, sd)
    
    breaks = [] # Array of the splits to keep
    range_indeces = list(unsup_ranges.keys())
    values = get_values(table, depIndex)
    
    def combine(lo, hi, values):
        #print("Looking from " + str(lo) + " to " + str(hi))
        best = statistics.stdev(values)
        cut = None
        cut_location = None
        n = len(values)
        
        # for each split:
        # - Get values to the left and right of split
        # - Calculate expected value of the split
        # - If split is better so far, set best and cut
        i = 0 
        for j in range(lo, hi):
            #print("--- Looking at spliting after range " + str(j))
            cur_bin_size = unsup_ranges[j]["n"]
            l = values[0:i+cur_bin_size]
            r = values[i+cur_bin_size:]
            i += cur_bin_size
            exp_val = (len(l)/n)*statistics.stdev(l) + (len(r)/n)*statistics.stdev(r)
            if exp_val < best:
                cut = j
                cut_location = i
                best = exp_val
        #print("Found best cut: " + str(cut) + "\n")

        # Recurse!
        if cut is not None:
            combine(lo,cut,values[0:cut_location])
            combine(cut+1,hi,values[cut_location:])
        else:
            breaks.append(hi)

    combine(range_indeces[0], range_indeces[len(range_indeces)-1], values)
    print("Break at the top of the following ranges: " + str(breaks))
    super_ranges = create_supers(unsup_ranges, breaks)
    printDictionary(super_ranges)

# Pass the ranges and indeces of ranges you want to break at the top of
def create_supers(unsup_ranges, splits):
    super_ranges = {}
    i = 1
    for key, u_range in unsup_ranges.items():
        if key in splits:
            super_ranges[i] = {"label":i, "most":u_range["high"]}
            i += 1
    return super_ranges
        
            
################ Helpers #####################
# Merge two bins - update the nested key values
# k1 is updated, k2 is set to None
def mergeBins(dict, k1, k2):
    dict[k1]['high'] = dict[k2]['high'] #merge update
    dict[k1]['span'] = dict[k1]['high']-dict[k1]['low']
    dict[k1]['n'] = dict[k1]['n'] + dict[k2]['n']
    dict[k2] = None # reset k2
    return dict

#print the dictionary
def printDictionary(dict):
    for key,value in dict.items():
        print(key)
        print(value)
    return

# return a list of random numbers 
# the size of the list = count, range for numbers = [min, max]
random.seed(5)
def randomNumRange(count, min, max):
    numList = []
    for x in range(0, count):
        numList.append(random.uniform(min, max))
    return numList

def get_values(table, colIndex):
    values = []
    for r in table.rows:
        row = table.rows[r]
        value = row.cells[colIndex]
        if value is not None:
            values.append(value)
    return values

################ Run #####################
# Create table
table = tbl.Tbl();
table.update({0:"$someNumeric"})
randomValues = randomNumRange(50,1, 23)
for i, val in enumerate(randomValues):
    y = .2
    if i > 5:
        y = .6
    if i > 30:
        y = .9
    table.update({0:val,1:y})

# Print table
for i, col in table.cols["all"].items():
    col.summarize()

# Run dicretizers
print("\n ================ UNSUPERVISED BINS ================")
ranges(table, 0)
print("\n ================ SUPERVISED BINS ================")
super_ranges(table, 0, 1)



