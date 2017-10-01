# Questions
# 1) It seems like we're doing a lot of column calculations! Don't want to 
#    have to get values from rows every time... is there a better way?
# 2) Should we redo the discretizer to be passed functions that extract
#    the independent and dependent values? This way we could pass it the
#    function that gets the dom values (since right now we just accept 
#    columns and dom is not a column)

import sys
sys.path.insert(0, '../part2')
sys.path.insert(0, '../part3')
import tbl
import create_bins
import statistics

# Command line args
#    1) fileName - name of file to build regression tree on
#    2) tooFew - stop splitting if there are this many or less examples
#    3) maxDepth - stop spliiting if the tree gets any deeper than this
# Example: python regression_trees.py ../part2/auto.csv 10 10

fileName = sys.argv[1]
tooFew   = int(sys.argv[2])
maxDepth = int(sys.argv[3])

# change the numeric values for a given col to the binID
def discretize_column(table, colIndex, superRanges):
    for r in table.rows:
        row = table.rows[r]
        value = row.cells[colIndex]
        for superRange in superRanges:
            if(value <= superRange["most"]):
                row.cells[colIndex] = superRange["label"] #replace the value with the id
                break # move to next row
            
# Apply supervised discretization to all independent columns
# Build Tree Recursively:
#    - Try spliting on ranges for each column
#    - Split on the column who reduces variability of dom
#    - Stop when:
#        - Spliting does not improve variability
#        - There are tooFew examples
#        - Depth is too much

################ Read table and discretize #####################
# Create fake table for now
table = tbl.Tbl()
table.fromCsv(fileName)
dom = table.dom()
for i, col in table.cols_x["nums"].items():
    s_ranges = create_bins.super_ranges(table, col.pos, "dom")
    #print(s_ranges)
    discretize_column(table, col.pos, s_ranges)
##table.update({0: "$indep1", 1: "$indep2"})#, 2:"$indep3"})
##rows = [{0: "1", 1: "2", 3: ""},
##        {0: "1", 1: "6", 3: ""},
##        {0: "2", 1: "6", 3: ""},
##        {0: "2", 1: "6", 3: ""},
##        {0: "4", 1: "7", 3: ""}]
##dom = {0:1, 1:2, 2:3, 3:3, 4:3}
##for row in rows:
##    table.update(row)

#for i, col in table.cols["all"].items():
    #col.summarize()

colList = list(table.cols_x["all"].keys())
rowList = list(table.rows.keys())

class Node():
    def __init__(self, rows):
        self.v = None
        self.depth = 0
        self.rows = rows
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
        for row in node.rows:
            cell = str(int(table.rows[row].cells[col]))
            if cell not in rowsByVal: # Create key if hasn't been created yet
                rowsByVal[cell] = []
            rowsByVal[cell].append(row)
        expVal = expValue(rowsByVal, len(node.rows))
        if (bestSplitCol is None) or (expVal < bestSplitVal):
            bestSplitCol = col
            bestSplitVal = expVal
            bestSplitRows = rowsByVal

    # Split on the column who reduces variability of dom
    # Stop when: Spliting does not improve variability
    nodeVariability = statistics.stdev(getDomsFromRows(node.rows))
    #print("... So should get " + str(nodeVariability))
    if bestSplitVal < nodeVariability: 
        node.splitOn = table.cols["all"][bestSplitCol].txt
        for key, rowArr in bestSplitRows.items():
            child = Node(rowArr)
            if len(rowArr) == 1:
                child.v = 0
            if len(rowArr) > 1:
                child.v = statistics.stdev(getDomsFromRows(rowArr))
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
    return domVals
    

def printTree(node):
    for key, child in node.children.items():
        for i in range(1, child.depth):
            sys.stdout.write('| ')
        sys.stdout.write(str(node.splitOn) + " = " + str(key) + "        ")
        sys.stdout.write('n = ' + str(len(child.rows)))
        sys.stdout.write(', mu = ' + str(statistics.mean(getDomsFromRows(child.rows))))
        sys.stdout.write(', sd = ' + str(child.v))
        sys.stdout.write('\n')
        printTree(child)

root = Node(rowList)
root.v = statistics.stdev(list(dom.values()))
split(root)
print()
printTree(root)

