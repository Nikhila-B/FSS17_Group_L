import sys
sys.path.insert(0, '../part4')
import regression_trees
import statistics 

# Branch Generator:
# Walk down the tree 
# 	and for each node 
# 		add the branch b to that node.out
def branches1(root, out, b):
	pass
def branches(root):
	return branches1(root, {}, {})

# Compute the delta between two branches
def delta(t1, t2):
	pass

# returns - two nodes per branch
# one branch with max improvement
# another branch with min improvement
def contrasts(branches, better):
	pass


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



