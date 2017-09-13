import sys

from datetime import datetime

start_time = datetime.now()

row_list = []
num_columns = []
sym_columns = []
approved_columns = []
skipped_rows = []

# Parses a data row (may be multiple lines) and adds the row to the row_list.
# TODO: I'd prefer not to pass the index, but it seems necessary to report the row in the error.
def parseRow(line, row_index):
    row = []
    for c in approved_columns:
        cell = line[c]
        if c == last_column: # Trim any comments
            cell = cell.split('#')[0]
        cell = cell.strip() # Trim white space
        if c in num_columns: # Convert numeric cells to float
            try:
                cell = float(cell)
            except ValueError:
                print("ERROR: Row " + str(row_index) + " has an invalid numeric cell " + str(c))
                skipped_rows.append(row_index)
                return
        row.append(cell)
    row_list.append(row)

# Process file
with open(sys.argv[1], 'r') as f:
    results = []
    for line in f:
        words = line.split(',')
        results.append(words)
    #print(results) # contains the list of rows
    headerlen = len(results[0])
    for i, column in enumerate(results[0]):
        magic_char = column.strip()[0]
        #TODO: Could have multiple magic characters, which would break this
        if magic_char == '$':
            num_columns.append(i)
        elif magic_char != '?':
            sym_columns.append(i)        

    # Get headers that should be included
    approved_columns = num_columns + sym_columns
    #approved_columns.sort() #TODO: necessary?

    # Convert the lists to tuples
    num_columns = tuple(num_columns)
    sym_columns = tuple(sym_columns)

    last_column = max(approved_columns)
    results = results[1:] # remaining list elements
    last_line = []
    # Read the data into the list     
    for i, line in enumerate(results):
            # Handle row split over multiple lines    
            if len(line) == 0: # empty lines are skipped
                continue
            if line[len(line)-1].strip() == "": # Row ends in comma
                last_line = last_line + line[:-1]
                continue
            if len(last_line):
                line = last_line + line
                last_line = [];
         
            # Skip rows where there's an incorrect number of cells
            if headerlen != len(line):
                skipped_rows.append(i)
                print("ERROR: Row " + str(i) + " has the wrong number of cells.")
                continue

            parseRow(line, i )
    
print("Number of rows/records read: " + str(len(row_list)))
print("Skipped rows: " + str(skipped_rows))
end_time = datetime.now() # Calculating run time
print('Duration: {}'.format(end_time - start_time))  
