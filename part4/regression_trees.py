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

# Command line args
#    1) fileName - name of file to build regression tree on
#    2) tooFew - stop splitting if there are this many or less examples
#    3) maxDepth - stop spliiting if the tree gets any deeper than this
# Example: python regression_trees.py ../parts/auto.csv 10 10

fileName = sys.argv[1]
tooFew   = sys.argv[2]
maxDepth = sys.argv[3]

# Apply supervised discretization to all independent columns
# Build Tree Recursively:
#    - Try spliting on ranges for each column
#    - Split on the column who reduces variability of dom
#    - Stop when:
#        - Spliting does not improve variability
#        - There are tooFew examples
#        - Depth is too much

################ Read table and discretize #####################
table = tbl.Tbl()
table.fromCsv(fileName)
for i, col in table.cols["all"].items():
    col.summarize()
print("\n================ UNSUPERVISED BINS ==================")
discretizer.ranges(table, 2)
print("\n================ SUPERVISED BINS ==================")
# TODO: should really be discretizing every column by dom
discretizer.super_ranges(table, 2, 7)

################ Recursively split table #####################


# Recursive function that splits... what should we pass it?
def split():
	pass
