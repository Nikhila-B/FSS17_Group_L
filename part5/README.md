## Output Explanation

Initally, our output was as shown in output.txt. At first glance, this may seem incorrect because it is expected to have n-squared comparisons, where n is the number of leaf nodes. We are doing this, but the output can be misleading. What we are outputting is the maximum delta and minimum delta (branch difference) of the comparisions of any node with all other nodes. In otherwords, a summary of the outer loop.

So, in output.txt, there are only n results shown, for both plans and monitors. 

To make this clearer, output_expanded.txt has the expanded output. In this output, we are printing which leaves are being compared, and whether a node is "better" than another. "Better" depends on whether a plan or monitor has been found, depending on which ever we are looking for at the time. Then we print whether there is a positive effect size test, and the delta between the branches of the nodes. Only plans or monitors that are distinct (effect size) and have a difference in delta make it to the comparisons discussed above in the output.txt.


## How to Run

To run, go to the part5 directory and run 'python contrast_sets.py ../part2/auto.csv 10 10'. These are the arguments for creating the tree. 

There is an example output in **output.txt**.


## Changes

* Added the statistics tests (hedges and ttest) in the num class of tbl.py from part 2. 
* Created create_sets.py in part5, which when run prints out the plans and monitors.
* Updating tree code from part 4 to be usable from contrast_sets.py

