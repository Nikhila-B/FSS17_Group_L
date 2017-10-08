### Files
* `run_trees.py` - file that discretizes num columns and runs table
* `regression_trees.py` - contains create_tree method to build and return the tree 

### Install Dependency
Please install the Statistics & Numpy Dependency package - we use it to calculate the standard deviation
* `python -m pip install Statistics`
* `python -m pip install numpy`

### How to Run
Navigate to ./part4 directory - `python run_trees.py ../part2/auto.csv 10 10`

Command line args
1. fileName - name of file to build regression tree on
2. tooFew - stop splitting if there are this many or less examples4
3. maxDepth - stop spliiting if the tree gets any deeper than this

### Output
The output.txt file contains the output of one sample run 

### How to Use
The tree code has been refactored for use outside of the file. To use, import 'regression_trees.py' and run create_tree(). This will return the root node which has an attribute 'print' which will print the tree.

Prerequisites: The create_tree function expects a table and parameters tooFew and maxDepth. Make sure that the num columns have been descretized.

