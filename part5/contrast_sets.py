import sys
sys.path.insert(0, '../part2')
sys.path.insert(0, '../part3')
sys.path.insert(0, '../part4')
import tbl
import create_bins
import statistics
import regression_trees

class Stats:
    def __init__(self, statsObj):
        self.n = statsObj["n"]
        self.sd = statsObj["sd"]
        self.mu = statsObj["mu"]

def has(branch_list):
    out = []
    for b in branch_list:
        out.append({"attr":b["attr"], "val":b["val"]})
    return out

def have(branches):
    for branch_obj in branches:
        branch_obj["has"] = has(branch_obj["branches"])
    return branches

# Adds all splits to out array
def branches1(node, out, b):
    if node.splitOn is not None:         
        for key, child in node.children.items():
            b.append({"attr":node.splitOn, "val":key, "stats":Stats(child.stats)})
            out.append({"has":None, "branches":b})
            branches1(child, out, list(b))
    return out

# Returns an array of branch dict which has properties:
# 1) has - array of splits, set in has
# 2) branches - array of branch objects, includes stats
def branches(node):
    return have(branches1(node, [], []))

# Compute the delta between two branches
def member(twin0, twins):
    for twin1 in twins:
        if twin0.attr == twin1.attr and twin0.val == twin1.att:
            return True
    return False
def delta(t1, t2):
    out = []
    for twin in t1:
        if not member(twin, t2):
            out.append((twin.attr, twin.val))
    return out

# returns - two branches per node
# one branch with max improvement
# another branch with min delta
def contrasts(branches, better):
    for i, branch1 in enumerate(branches):
        out = []
        for j, branch2 in enumerate(branches):
            if i != j:
                num1 = branch1["branches"][-1]["stats"]
                num2 = branch2["branches"][-1]["stats"]
                if better(num2.mu, num1.mu): #RULE1
                    if not tbl.Num.same(num1, num2): #RULE2
                        inc = delta(branch2.has, branch1.has)
                        if len(inc) > 0: #RULE3
                            out.append({i:i, j:j, ninc:len(inc),
                                        muinc:num2.mu-num1.mu, inc:inc,
                                        branch1:branch1.has, mu1:num1.mu,
                                        branch2:branch2.has, mu2:num2.mu})
        if len(out) <= 0:
            print("Error: out is empty")
        else:
            sorted(out, key=lambda x, y: x.muinc > y.muinc)
            print(str(i)+ " max mu: " + out[0])
            sorted(out, key=lambda x, y: x.ninc < y.ninc)
            print(str(i)+ " min inc: " + out[0])
        


# Plans - things we want to do - More Value
# Monitors - things we want to avoid _ Less value
def more(x,y):
    return x > y
def less(x,y):
    return x < y
def plans(branches):
    return contrasts(branches, more)
def monitors(branches):
    return contrasts(branches, less)

#################################### RUN ######################################
# Command line args
#    1) fileName - name of file to build regression tree on
#    2) tooFew - stop splitting if there are this many or less examples
#    3) maxDepth - stop spliiting if the tree gets any deeper than this
# Example: python contrast_sets.py ../part2/auto.csv 10 10
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

bs = branches(root)
plans(bs)
monitors(bs)


