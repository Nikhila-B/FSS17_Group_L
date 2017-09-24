### Output
The `output.txt` file contains the output of one run of create_bins.py. All the bins are printed from unsupervised and supervised discretization.

**Update:** `output.txt` is the output after correcting how the test data is generated. The dependent variable is now actually dependent on the independent variable, and matches the example test code. Test data is no longer uniform or seeded. 


### File
 `create_bins.py`
* Sections
  * Unsupervised Discretization Section
  * Supervised Discretization  Section
  * Helper Method Section  
  * Run 
    * Both unsupervised and supervised discretization are run on generated data. As in the test code example, there is an independent variable with 50 values zero to one, and an dependent variable that is related to that independent variable.

### Install Dependency
Please install the Statistics Dependency package - we use it to calculate the standard deviation
`python -m pip install statistics`
### To Run 
In order to run, navigate to the terminal where **create_bins.py** file is located and run `python create_bins.py`

