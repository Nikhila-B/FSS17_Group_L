import sys
sys.path.insert(0, '../part2')
sys.path.insert(0, '../part3')
import tbl
import create_bins
import statistics
import regression_trees

# Command line args
#    1) fileName - name of file to build regression tree on
#    2) tooFew - stop splitting if there are this many or less examples
#    3) maxDepth - stop spliiting if the tree gets any deeper than this
# Example: python run_trees.py ../part2/auto.csv 10 10
fileName = sys.argv[1]
tooFew   = int(sys.argv[2])
maxDepth = int(sys.argv[3])

# change the numeric values for a given col to the binID
def discretize_column(table, colIndex, superRanges):
    for r in table.rows:
        row = table.rows[r]
        value = row.cells[colIndex]
        if value is not None:
            for superRange in superRanges:
                if value <= superRange["most"]:
                    row.cells[colIndex] = int(superRange["label"]) #replace the value with the id
                    break # move to next row
                
table = tbl.Tbl()
table.fromCsv(fileName)
dom = table.dom()
for i, col in table.cols_x["nums"].items():
    s_ranges = create_bins.super_ranges(table, col.pos, "dom")
    print(s_ranges)
    discretize_column(table, col.pos, s_ranges)

root = regression_trees.create_tree(table, tooFew, maxDepth)
print("------------- Printing tree -----------------")
root.print()



