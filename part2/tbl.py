import math

class Tbl:

    def __init__(self):
        pass
        # init instance vars

    # Read in CSV file, call update on every row
    # Make sure handles multiple lines
    def fromCsv(self, fileName):
        pass

    # Update the table with a row
    # Calls header for first row, data for rest
    def update(self, cells):
        pass

    # Create headers from first row of table
    # Calls categories to get spec for the column
    def header(self, cells):
        pass

    # Looks for special characters in the header text and returns spec for the special character
    # headerTxt - column header text to parse
    def categories(self, headerTxt):
        pass

    # Create new Row and update
    # In lua, something called old for (I think) updating rows. Don't worry about it for now.
    def data(self, cells):
        pass


class Row:
    
    def __init__(self):
        pass
        # Initialize id and cells[]

    # Update the table headers
    def update(self, cells, table):
        pass

    # Get domination score for row, by comparing all pairs of rows
    def dominate(self):
        pass

    # i.e. dominate1
    # subrouting of dominate that determines if this row dominates otherRow
    @staticmethod
    def dominationCompare(r1, r2):
        pass

    # Calculate distance between two rows
    @staticmethod
    def distance(r1, r2):
        pass
        
#TODO fill out
class Num:

    def __init__(self):
        self.n = 0 #Total number of cells
        self.mu = 0
        self.m2 = 0
        self.sd = 0 #standard deviation
        self.high = (-math.exp(32)) #Heightest Value in the column
        self.low = (math.exp(32)) #Lowest value in the column
        self.weight = 1 #weight of the column

    # Add a new value to the column, and update column stats
    def update(self, newVal):
        # update count, lo, hi, sd
        self.n += 1 #increasing the counter for each new value
        if newVal < self.low:
            self.low = newVal
        if newVal > self.high:
            self.high = newVal
        delta = newVal - self.mu
        self.mu += delta/self.n
        self.m2 += delta*(newVal - self.mu)
        if self.n > 1:
            self.sd = (self.m2/(self.n - 1))**0.5
        return

    # Return the normalized value
    def norm(self, val):
        return (val - self.low)/(self.high - self.low + math.exp(-32))

    # Return the distance between two nums
    # Lua - something about watcher?
    #@staticmethod
    def distance(self, n1, n2):
        if n1 is None and n2 is None:
            return 0
        elif n1 is None:
            n2 = self.norm(n2)
            n1 = 1 if n2 < 0.5 else 0
        elif n2 is None:
            n1 = self.norm(n1)
            n2 = 1 if n1 < 0.5 else 0
        else:
            n1 = self.norm(n1)
            n2 = self.norm(n2)
        return abs(n1-n2)**2


class Sym:

    def __init__(self):
        self.n = 0 # total number of cells
        self.nk = 0 # count of distinct values
        self.counts = {} # dictionary of value counts
        self.most = 0 # count of value that appears most
        self.mode = None # value that appears most
        self._ent = None # entropy, not calculated on update
        pass

    # Add a new value to the column, and update column stats
    def update(self, newVal):
        self._ent = None # "zap" entropy
        self.n = self.n + 1
        if newVal not in self.counts:
            self.nk = self.nk + 1
            self.counts[newVal] = 0
        seen = self.counts[newVal] + 1
        self.counts[newVal] = seen
        if seen > self.most:
            self.most, self.mode = seen, newVal
        

    # Return the normalized value
    def norm(self, val):
        return val

    # Returns two numbers x,y where x is the distance and y is 0,1
    #    depending on whether or not we are returning nothing.
    # If either is unknown, the return the max possible distance.
    # If both are unknown, just return nothing.
    @staticmethod
    def distance(s1, s2):
        if s1 is None and s2 is None:
            return (0, 0) # Return nothing
        if s1 == s2:
            return (0, 1)
        else:
            return (1, 1) # Includes case where one is None

    # Return (and set) the entropy calculation of the column
    def ent(self):
        #cache
        if self._ent is None:
            e = 0
            for name, count in self.counts.items():
                p = count/self.n
                e = e - (p * math.log(p, 2))
            self._ent = e
        return self._ent

    # Prints the stats for the row, for testing
    def summarize(self):
        print("Count: " + str(self.n))
        print("Distinct count: " + str(self.nk))
        print("Same counts: ")
        for value in self.counts:
            print ("    " + value + ": " + str(self.counts[value]))
        print("Most: " + str(self.most))
        print("Mode: " + str(self.mode))
        print("Entropy: " + str(self._ent))
        
        
    
