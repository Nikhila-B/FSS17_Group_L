### File
 `create_bins.py`
* Unsupervised Discretization Section
* Supervised Discretization  Section
* Helper Method Section  
* Run 
  * Input Data - Currently generating 100 numbers in the range[1, 23]. These parameters can be changed in the notes.

### To Run 
In order to run, navigate to the terminal where **create_bins.py** file is located and `python ./create_bins.py`

### Output
Output is directed to the `output.txt` file. 
* All the bins and the bin stats are printed from unsupervised discretization
* Supervised discretization bins are also printed
   * Unsupervised bins are inspected and a decision to whether to keep the bin split is made after looking at the dependent variable- [the subset of splits]
