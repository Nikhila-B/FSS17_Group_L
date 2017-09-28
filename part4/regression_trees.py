# Questions
# 1) It seems like we're doing a lot of column calculations! Don't want to 
#    have to get values from rows every time... is there a better way?
# 2) Should we redo the discretizer to be passed functions that extract
#    the independent and dependent values? This way we could pass it the
#    function that gets the dom values (since right now we just accept 
#    columns and dom is not a column)

import sys
sys.path.insert(0, '../part2')
import tbl
import discretizer
import statistics

# Command line args
#    1) fileName - name of file to build regression tree on
#    2) tooFew - stop splitting if there are this many or less examples
#    3) maxDepth - stop spliiting if the tree gets any deeper than this
# Example: python regression_trees.py ../part2/auto.csv 10 10

fileName = sys.argv[1]
tooFew   = int(sys.argv[2])
maxDepth = int(sys.argv[3])

# Apply supervised discretization to all independent columns
# Build Tree Recursively:
#    - Try spliting on ranges for each column
#    - Split on the column who reduces variability of dom
#    - Stop when:
#        - Spliting does not improve variability
#        - There are tooFew examples
#        - Depth is too much

################ Read table and discretize #####################

#table.fromCsv(fileName)
#print("\n================ UNSUPERVISED BINS ==================")
#discretizer.ranges(table, 2)
#print("\n================ SUPERVISED BINS ==================")
#discretizer.super_ranges(table, 2, 7)

# Create fake table for now
table = tbl.Tbl()
table.update({0: "$indep1", 1: "$indep2"})
rows = [{0: "1", 1: "2", 3: "1"},
        {0: "1", 1: "3", 3: "2"},
        {0: "2", 1: "2", 3: "1"},
        {0: "2", 1: "3", 3: "2"},
        {0: "2", 1: "4", 3: "1"}]
dom = {0:1,1:2,2:1,3:2,4:1}
for row in rows:
    table.update(row)

for i, col in table.cols["all"].items():
    col.summarize()

colList = list(table.cols["all"].keys()) # only independent
rowList = list(table.rows.keys())

class Node():
    def __init__(self, values):
        self.v = None
        self.depth = 0
        self.values = values
        self.splitOn = None # Column id that node was split on
        self.children = {} # Dictionary (by bin id) of chlid nodes

################ Recursively split table #####################
def expValue(rowsByVal, n):
    expVal = 0
    for key, rowArr in rowsByVal.items():
        l = len(rowArr)
        if l == 1:
            sd = 0
        else:
             sd = statistics.stdev(getDomsFromRows(rowArr))
        expVal += sd * (l/n)
    return expVal
    
def split(node):
    
    bestSplitCol = None
    bestSplitDict = None
    bestSplitVal = None
    # Try spliting on ranges for each column
    for col in colList:
        if col == node.splitOn:
            return
        rowsByVal = {} # Dictonary to find rows for each different column value
        for row in node.values:
            cell = str(int(table.rows[row].cells[col]))
            if cell not in rowsByVal: # Create key if hasn't been created yet
                rowsByVal[cell] = []
            rowsByVal[cell].append(row)
        expVal = expValue(rowsByVal, len(node.values))
        if (bestSplitCol is None) or (expVal < bestSplitVal):
            bestSplitCol = col
            bestSplitVal = expVal
            bestSplitRows = rowsByVal

    # Split on the column who reduces variability of dom
    # Stop when: Spliting does not improve variability
    nodeVariability = statistics.stdev(getDomsFromRows(node.values))
    node.v = nodeVariability
    if bestSplitVal < nodeVariability: 
        node.splitOn = table.cols["all"][bestSplitCol].txt
        for key, rowArr in bestSplitRows.items():
            child = Node(rowArr)
            child.depth = node.depth + 1
            node.children[key] = child

            # Stop when:
            #   - Spliting does not improve variability (see outer if)
            #   - There are tooFew examples
            #   - Depth is too much
            if (len(rowArr) > tooFew) and (node.depth < maxDepth):
                split(child)

def getDomsFromRows(rowsList):
    domVals = []
    for row in rowsList:
        domVals.append(dom[row])
    print(domVals)
    return domVals
    

def printTree(node):
    for key, child in node.children.items():
        for i in range(1, child.depth):
            sys.stdout.write('| ')
        sys.stdout.write(str(node.splitOn) + " = " + str(key) + "        ")
        sys.stdout.write('n = ')
        sys.stdout.write(str(len(child.values)))
        sys.stdout.write(', mu = ')
        sys.stdout.write(str(statistics.mean(child.values)))
        sys.stdout.write(', sd = ')
        sys.stdout.write(str(child.v))
        sys.stdout.write('\n')
        printTree(child)

root = Node(rowList)
root.v = statistics.stdev(list(dom.values()))
split(root)
print()
printTree(root)



        
#    - Split on the column who reduces variability of dom
#    - Stop when:
#        - Spliting does not improve variability
#        - There are tooFew examples
#        - Depth is too much
