import sys
import math

class Range:
    def __init__(self):
        self.n = 0
        self.hi = sys.maxsize
        self.lo = -(sys.maxsize - 1)
        self.span = sys.maxsize

    def get_ranges(self, numList):
        # Sort
        numList = sorted(numList)
        print(numList)
        # Break into bins of size sqrt(N)
        minBinSize = math.sqrt(len(numList))
        # is numlist going to be 
        espsilon = 0.2*numlist.sd
        # Clean bins

    
class Super:
    def something():
        pass
