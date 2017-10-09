import math
import csv_reader

class Tbl:

    def __init__(self):
        self.rows = {}
        self.spec = {}
        self.goals = {}
        self.less = {}
        self.more = {}
        self.name = {}

        self.cols = { "nums":{}, "syms":{}, "all":{} }
        self.cols_x = { "nums":{}, "syms":{}, "all":{} }
        self.cols_y = { "nums":{}, "syms":{}, "all":{} }
        
    # Read in CSV file, call update on every row
    # Make sure handles multiple lines
    def fromCsv(self, fileName):
        csv_callback = lambda cells: self.update(cells)
        csv_reader.withEachLine(fileName,csv_callback)

    # Update the table with a row
    # Calls header for first row, data for rest
    def update(self, cells):
        if len(self.spec) == 0:
            self.header(cells)
        else:
            self.data(cells);
        
    # Create headers from first row of table
    # Calls categories to get spec for the column
    def header(self, cells):
        self.spec = cells
        for index, cell in cells.items():
            info = self.categories(cell)
            header_instance = info["what"]()
            header_instance.pos = index
            header_instance.txt = cell
            header_instance.weight = info["weight"]
            self.name[header_instance.txt] = header_instance
            for col_dict in info["included_in"]:
                col_dict[header_instance.pos] = header_instance
            

    # Looks for special characters in the header text and returns spec for the special character
    # headerTxt - column header text to parse
    def categories(s, headerTxt):
        spec =  {
            "$":{ "what": Num, "weight": 1, "included_in": [ s.cols["all"], s.cols_x["all"], s.cols["nums"], s.cols_x["nums"] ]},
            "<":{ "what": Num, "weight":-1, "included_in": [ s.cols["all"], s.cols_y["all"], s.cols["nums"], s.cols_y["nums"], s.goals, s.less ]},
            ">":{ "what": Num, "weight": 1, "included_in": [ s.cols["all"], s.cols_y["all"], s.cols["nums"], s.cols_y["nums"], s.goals, s.more ]},
            "!":{ "what": Sym, "weight": 1, "included_in": [ s.cols["all"], s.cols_y["all"], s.cols["syms"], s.cols_y["syms"] ]},
            "": { "what": Sym, "weight": 1, "included_in": [ s.cols["all"], s.cols_x["all"], s.cols["syms"], s.cols_x["syms"] ]}
        }
        for key, value in spec.items():
            if key in headerTxt:
                return value
        

    # Create new Row and update with cells
    # In lua, something called old for (I think) updating rows. Don't worry about it for now.
    def data(self, cells):
        row = Row()
        try:
            row.update(cells, self)
            self.rows[row.rid] = row
        except:
            print("Skipping row: " + str(cells))
            pass

    def dom(self):
        dom_dict = {}
        for i,row in self.rows.items():
            if row.rid not in dom_dict:
                wins = row.dominate(self)
                dom_dict[row.rid] = wins
        sorted_keys = sorted(dom_dict, key=lambda i: int(dom_dict[i]), reverse=True)
        show_num = 5
        top = sorted_keys[:show_num]
        bottom = sorted_keys[-show_num:]
            
        print()
        print("DOMINATION RESULTS")
        print("Header" + str(self.spec))
        print("----- TOP -----")
        for k in top:
            print(self.rows[k].cells)
        print("----- BOTTOM -----")
        for k in bottom:
            print(self.rows[k].cells)
        self.doms = dom_dict
        return dom_dict

      
class Row:

    curID = 0

    @staticmethod
    def getID():
        newID = Row.curID
        Row.curID += 1
        return newID
    
    def __init__(self):
        self.rid = Row.getID()
        self.cells = {}

    # Update the table headers
    def update(self, cells, table):
        colsIter = table.cols["all"].items()
        # Convert cells from string, if applicable. If it fails, skip the row
        for i,header in colsIter:
            try:
                cells[header.pos] = header.fromString(cells[header.pos])
            except:
                raise
        # Update the headers
        for i,header in colsIter:
            header.update(cells[header.pos])
            self.cells = cells
        

    # Get domination score for row, by comparing all pairs of rows
    def dominate(self, t):
        wins = 0
        for i,row in t.rows.items():
            if self.rid != row.rid:
                if self.dominationCompare(row, t):
                    wins += 1
        return wins

    # i.e. dominate1
    # subrouting of dominate that determines if this row dominates otherRow
    def dominationCompare(self, other_row, t):
        n = len(t.goals)
        sum1, sum2 = 0,0
        for k, col in t.goals.items():
            w = col.weight
            x = col.norm(self.cells[col.pos])
            y = col.norm(other_row.cells[col.pos])
            sum1 = sum1 - math.e**(w * (x-y)/n)
            sum2 = sum2 - math.e**(w * (y-x)/n)
        return sum1/n < sum2/n
        


    # Calculate distance between two rows
    @staticmethod
    def distance(r1, r2, t):
        d,n,p = 0,10^-64,0.5
        for i,col in t.x_cols["all"].items():
            d1, n1 = col.distance(r1.cells[col.pos], r2.cells[col.pos])
            d = d + d1
            n = n + n1
        return d**p / n**p

        
class Num:
    #dictionary of num properties - declared in config file for lua
    # https://lualure.github.io/info/config

    def __init__(self):
        self.n = 0 #Total number of cells
        self.mu = 0
        self.m2 = 0
        self.sd = 0 #standard deviation
        self.high = (-math.exp(32)) #Heightest Value in the column
        self.low = (math.exp(32)) #Lowest value in the column
        self.weight = 1 #weight of the column TODO isn't this covered in spec?
        self.num ={'conf' : 95,
                   'small' : 0.38,
                   'first' : 3,
                   'last' : 96,
                   'criticals ' : {
                       '[95]': {'[3]': 3.182, '[6]': 2.447, '[12]': 2.179,
                                '[24]': 2.064, '[48]': 2.011, '[96]': 1.985},
                       '[99]': {'[3]': 5.841, '[6]': 3.707, '[12]': 3.055,
                                '[24]': 2.797, '[48]': 2.682, '[96]': 2.625}
                        }
                   }

    # Add a new value to the column, and update column stats
    def update(self, newVal):
        if newVal is None:
            return    
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
        return abs(n1-n2)**2,1

    def fromString(self, value):
        try:
            if value is not None:
                return float(value)
        except:
            print("Error: Invalid float value: " + value)
            raise

    def summarize(self):
        print()
        print("------- NUM -------")
        print("Name: " + str(self.txt))
        print("Count: " + str(self.n))
        print("SD: " + str(self.sd))
        print("High: " + str(self.high))
        print("Low: " + str(self.low))

    # Hedges test from num class - Effect Size test
    @staticmethod
    def hedges(i,j):
        nom   = (i.n - 1)*i.s**2 + (j.n - 1)*j.s**2
        denom = (i.n - 1) + (j.n - 1)
        sp    = ( nom / denom )**0.5
        delta = abs(i.mu - j.mu) / sp
        c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
        return delta * c < 0.38

    # Helper method for the significance test -  ttest below
    @staticmethod
    def ttest1(df,first,last,crit):
        if df <= first:
            ## in order to access the value for the 95th confidence [3] key
            key = "" + first + ""
            crit[key] ## need to check this call - dictionary
        elif  df >= last:
            ## in order to access the value for the 95th confidence [3] key
            key = "" + last + ""
            crit[last]
        else:
            n1 = first
            while n1 < last:
                n2=n1*2
                if df >= n1 and df <= n2:
                    old,new = crit[n1],crit[n2] #is this legal in python
                    return old + (new-old) * (df-n1)/(n2-n1)
                n1=n1*2
        return n1 # is this what we should be returning?

    # ttest from num class - Significance test
    @staticmethod
    def ttest(i, j):
        t = (i.mu -j.mu)/math.sqrt(max(1e-64, i.sd**2/i.n + j.sd**2/j.n ))
        a = i.sd**2/i.n
        b  = j.sd**2/j.n
        df = (a + b)**2 / (1e-64 + a**2/(i.n-1) + b**2/(j.n - 1))
        c  = Num.ttest1(math.floor( df + 0.5 ), Num.num["first"], Num.num["last"],Num.num["criticals"]["[95]"]) # check the last argument??
        return math.abs(t) > c

    # checks for both hedges test and ttest
    @staticmethod
    def same(i,j):
        return not (Num.hedges(i,j) and Num.ttest(i, j))


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
    def distance(self, s1, s2):
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

    def fromString(self, value):
        return value

    # Prints the stats for the row, for testing
    def summarize(self):
        print()
        print("------- SYM -------")
        print("Name: " + str(self.txt))
        print("Count: " + str(self.n))
        print("Distinct count: " + str(self.nk))
        print("Same counts: ")
        for value in self.counts:
            print ("    " + value + ": " + str(self.counts[value]))
        print("Most: " + str(self.most))
        print("Mode: " + str(self.mode))
        print("Entropy: " + str(self._ent))
        
        
    
