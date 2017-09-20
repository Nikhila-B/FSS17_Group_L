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

# May be in our case we can create column data list
def make_bins(numList):
    numList.sort()
    n = len(numList)
    minBinSize = math.sqrt(n)
    espilon = 0.2*statistics.stdev(numList)
  
    #initialize the first bin
    low = numList(0)
    high = numList(minBinSize)
    span = high - low
    
    #traverse from sqrt(n)th item onwards and see if it needs to be split
    for item in range(minBinSize, n)
        #(1) >=minBinsize
        #(2) ranges differ by epsilon
        #(3) span of range > epsilon
        #(4) low is greater than hi of prev range
        while(e)


    pass


fullList = randomNumRange(10,1, 23)
make_bins(fullList)
