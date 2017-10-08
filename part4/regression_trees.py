import sys
import statistics

# Apply supervised discretization to all independent columns
# Build Tree Recursively:
#    - Try spliting on ranges for each column
#    - Split on the column who reduces variability of dom
#    - Stop when:
#        - Spliting does not improve variability
#        - There are tooFew examples
#        - Depth is too much
def create_tree(table, tooFew, maxDepth):

    class Node():
        def __init__(self, rows):
            self.isRoot = False
            self.v = None
            self.depth = 0
            self.rows = rows
            self.splitOn = None # Column id that node was split on
            self.children = {} # Dictionary (by bin id) of chlid nodes

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
                cell = table.rows[row].cells[col]
                if cell is None:
                    continue
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
                if len(rowArr) < tooFew:
                    continue
                child = Node(rowArr)
                child.v = statistics.stdev(getDomsFromRows(rowArr))
                child.depth = node.depth + 1
                node.children[key] = child

                # Stop when:
                #   - Spliting does not improve variability (see outer if)
                #   - There are tooFew examples
                #   - Depth is too much
                if node.depth < maxDepth:
                    split(child)
                    

    def getDomsFromRows(rowsList):
        domVals = []
        for row in rowsList:
            domVals.append(dom[row])
        return domVals
        

    def printTree(node):
        if node.isRoot is True:
            domValues = getDomsFromRows(node.rows)
            print("\nin=" + str(len(domValues))
              + " mu=" + str(round(statistics.mean(domValues),2))
              + " sd=" + str(round(node.v,2)))
        for key, child in sorted(node.children.items()):
            for i in range(1, child.depth):
                sys.stdout.write('| ')
            
            sys.stdout.write(str(node.splitOn) + " = " + str(key))
            if len(child.children) == 0:
                sys.stdout.write('        n = ' + str(len(child.rows)))
                mu = statistics.mean(getDomsFromRows(child.rows))
                sys.stdout.write(', mu = ' + str(round(mu, 2)))
                sys.stdout.write(', sd = ' + str(round(child.v,2)))
            sys.stdout.write('\n')
            printTree(child)

    dom = table.doms
    colList = list(table.cols_x["all"].keys())
    rowList = list(table.rows.keys())
    root = Node(rowList)
    domValues = list(dom.values())
    root.v = statistics.stdev(domValues)
    root.isRoot = True
    
    split(root)
    root.print = lambda: printTree(root)
    return root

