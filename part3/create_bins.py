import sys
#sys.stdout = open('output.txt', 'w')
sys.path.insert(0, '../part2')
import tbl
import math
import random
import statistics
import numpy

################ Unsupervised Discretization #####################

def ranges(table, colIndex):
    indep_values = get_values(table, colIndex)
    col = table.cols["all"][colIndex]
    sd = statistics.stdev(indep_values)
    indep_values.sort()
    unsup_bins = make_bins(indep_values, sd)
    return unsup_bins

# Expects already sorted list
def make_bins(numList, sd):

    # Initalize bin variables
    n = len(numList)
    epsilon = 0.2*statistics.stdev(numList)
    print("Epsilon: " + str(epsilon))
    minBinSize = math.ceil(math.sqrt(n))
    numInitBins = math.floor(n/minBinSize) #total number of initial bins

    #(1) >=minBinsize
    #(2) ranges differ by epsilon
    #(3) span of range > epsilon
    #(4) low is greater than hi of prev range

    # Create bins (1) that are >= minBinSize
    bins = []
    cur_pos = 0
    for i in range(1, numInitBins+1):
            start = cur_pos
            end = cur_pos + minBinSize -1 #inclusive
            bin_dict = {}
            bin_dict['low'] = numList[start]
            bin_dict['high'] = numList[end]
            bin_dict['span'] = bin_dict['high'] - bin_dict['low']
            bin_dict['n'] = minBinSize
            # in case there are fewer elements than minBinsSize at the end
            # add it to the last bin
            if(i == numInitBins and end < n-1):
                bin_dict['high'] = numList[n-1]
                bin_dict['span'] = bin_dict['high'] - bin_dict['low']
                bin_dict['n'] = minBinSize + ((n-1)-end)
            bins.append(bin_dict)
            cur_pos = cur_pos + minBinSize

    # Traverses bins and combines bins if they match conditionFunc
    def combine_bins(conditionFunc):

        def stop_merging(arr):
            return len(arr) <= 1

        i = 0
        while i < len(bins):
            if i == len(bins)-1:
                while not stop_merging and conditionFunc(bins[i-1], bins[i]):
                    merge_bins(i-1, 1)
                    i -= 1 # If you've deleted the last, now look at what you just merged into
            else:
                while not stop_merging and conditionFunc(bins[i], bins[i+1]):
                    merge_bins(i, i+1)
            i += 1

    # Merge second bin into the first bin
    def merge_bins(i1, i2):
        bin1, bin2 = bins[i1], bins[i2]
        bin1['high'] = bin2['high']
        bin1['span'] = bin2['high'] - bin1['low']
        bin1['n'] = bin1['n'] + bin2['n']
        del bins[i2]

    # Print bins before checks
    print("\n--- Before combining ---")
    for bin_dict in bins:
        print(bin_dict)

    # (2)?
            
    # (3) Combine bins if the span is less than some epsilon
    combine_bins(lambda b, placeholder: b['span'] < epsilon )

    # (4) low is greater than hi of prev range (would only combine if they are equal)
    combine_bins(lambda b1, b2: b2['low'] < b1['high'] )

    # Print bins after checks
    print("\n--- After combining: END of Unsupervised  ---")
    for bin_dict in bins:
        print(bin_dict)
    print()

    return bins

        
################ Supervised Discretization #####################

def super_ranges(table, colIndex, depIndex):
    
    values = get_value_pairs(table, colIndex, depIndex)
    values.sort() #sort pairs on indep value
    numpyValues = numpy.array(values)

    # Get unsupervised bins
    sd = table.cols["all"][colIndex].sd
    unsup_ranges = make_bins(numpyValues[:,0], sd)
    
    breaks = [] # Array of the splits to keep
    def combine(lo, hi, depList):
        print("Looking from i = " + str(lo) + " to " + str(hi))

        # Start with full list
        best = statistics.stdev(depList)
        cut = None
        cut_location = None
        n = len(depList)

        print("Original best: " + str(best))
        
        # for each split:
        # - Get values to the left and right of split
        # - Calculate expected value of the split
        # - If split is better so far, set best and cut
        i = 0
        for j in range(lo, hi):
            print("--- Looking at spliting after range " + str(j))
            cur_bin_size = unsup_ranges[j]["n"]
            left = depList[0:i+cur_bin_size]
            right = depList[i+cur_bin_size:]
            print("--- Left size: " + str(len(left)))
            print("--- Right size: " + str(len(right)))
            i += cur_bin_size
            exp_val = ((len(left)/n)*statistics.stdev(left)) + ((len(right)/n)*statistics.stdev(right))
            if exp_val < best:# and best-exp_val > 10e-1:
                cut = j
                cut_location = i
                best = exp_val
                print("Found new best: " + str(best))
        print("Found best cut: " + str(cut) + "\n")

        # Recurse!
        if cut is not None:
            combine(lo,cut,depList[0:cut_location])
            combine(cut+1,hi,depList[cut_location:])
        else:
            breaks.append(hi) # apending the bin id

    # TODO - someone double check the first call arguments?
    combine(0, len(unsup_ranges)-1, numpyValues[:,1]) # [ 0 - first bin, n - last bin, depList values]
    super_ranges_list = create_supers(unsup_ranges, breaks)
    
    print("Printing before ranges.")
    i = 0
    for j in unsup_ranges:
        n = j["n"]
        print(numpyValues[:,1][i:i+n])
        i += n

    print("\nPrinting after ranges.")
    start = 0
    last = 0
    for i, bin_dict in enumerate(unsup_ranges):
        n = bin_dict["n"]
        if(i in breaks):
            print(numpyValues[:,1][start:last+n])
            start = last + n
        last += n
    
    return super_ranges_list
    

# Pass the ranges and indeces of ranges you want to break at the top of
def create_supers(unsup_ranges, splits):
    super_ranges_list = []
    splits.sort()
    i = 1
    for split in splits:
        values = {}
        values['label'] = i
        values['most'] = unsup_ranges[split]["high"]
        super_ranges_list.append(values)
        i += 1
    return super_ranges_list
    

################ Helpers #####################
#print the dictionary
def printDictionary(dictionary):
    for key,value in dictionary.items():
        print(str(key) + ": " + str(value))
    return

# return a list of random numbers
# the size of the list = count, range for numbers = [0,1]
# Comment out seed: random.seed(5)
def randomList(count):
    numList = []
    for x in range(0, count):
        numList.append(random.random())
    return numList

def get_values(table, colIndex):
    values = []
    for r in table.rows:
        row = table.rows[r]
        value = row.cells[colIndex]
        if value is not None:
            values.append(value)
    return values

def get_value_pairs(table, colIndex, depIndex):
    values = []
    for r in table.rows:
        row = table.rows[r]
        indep = row.cells[colIndex]
        if indep is not None:
            if depIndex == "dom":
                dep = table.doms[r]
            else:   
                dep = row.cells[depIndex]
            values.append([indep, dep])
    return values


################ Run #####################
# Create table
table = tbl.Tbl();
table.update({0:"$someNumeric"})
randomValues = randomList(50)
for val in randomValues:
    #r = 2*random.random()/100
    r = 0
    #print(r)
    if val < .2:
        y = .2 + r
    elif val < .6:
        y = .6 + r
    else:
        y = .9 + r
    #print(val,y)
    row = {0:val,1:y}
    table.update(row)

# Print table
#for i, col in table.cols["all"].items():
#col.summarize()


# Run dicretizers
#print("\n================ UNSUPERVISED BINS ================")
#ranges(table, 0)
#print("\n================ SUPERVISED BINS ==================")
supers = super_ranges(table, 0, 1)

