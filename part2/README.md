## Output

The output of the domination function can be found in output.txt. The header is printed first, which shows which dictionary key corresponds to which column. Then the five top and bottom domination rows are printed, as dictionaries. If necessary, use the header to find which column the key corresponds to.

## How to run

To run the domination function, run tbl_test.py with the .csv/.txt filePath as a command. This will print information about the columns first, followed by the domination output. The domination function takes a few seconds, and is printed a few seconds after everything else.

tbl_test.py reads a table from a csv file, whose name is passed in, using the Tbl class's fromCSV function. Then, it runs the table's dom function, which sorts the rows by their domination scores and prints out the top and bottom five rows.

## Files

### output.txt
This file contains the domination output.

### tbl_test.py
This is the file that uses and tests the table classes. Currently, it prints information about the table, and at the end prints the domination results.

### tbl.py
This is a python module that contains the following classes: Tbl, Row, Sym, Num. Together, these classes make up the components of a table. For more details, see the documentation in the code.

### csv.py
This file contains helper functions to read in csv files. It is used by Tbl to read in a table line by line.
