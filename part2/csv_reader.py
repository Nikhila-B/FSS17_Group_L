first_line = True
header_length = None
ignored_columns = []
fext = ['txt', 'csv'] # File extensions allowed

# Helper function that determines if a line (string) is incomplete
# Returns True if the line ends in a comma, false otherwise
def incompleteLine(txt):
    return txt[-1:] == ','

# Helper function that determines if a column should be ignored
# Returns true if the col name includes "?", false otherwise
def ignoreCol(txt):
    return txt.find("?") == 0


# Helper function that cleans a line
# Check each line - remove padding and comments
def cleanLine(txt):
    txt = txt.split('#')
    txt = txt[0].strip()
    return txt

# Reads through the file line by line, converts each line to a cell dictionary which it
# passes to the function argument, fn
def withEachLine(fileName, fn):
    
    global first_line
    last_cells = []

    if (fileName.strip()[-3:] in fext for s in fext):
       with open(fileName, 'r') as f:

            for line in f:

                # Clean the line  
                line = cleanLine(line) # remove comments and padding
                if len(line) == 0: # skip empty rows
                    continue

                cells = line.split(",")
                
                # Handle rows split over multiple lines
                if incompleteLine(line):
                    last_cells = last_cells + cells[:-1]
                    continue
                if len(last_cells):
                    cells = last_cells + cells
                    last_cells = []

                # Check for correct length (or set correct length, if on first line)
                if first_line:
                    header_length = len(cells)
                else:
                    if len(cells) != header_length:
                        print("Error: incorrect number of cells: " + str(len(cells)))
                        print("Skipping row: " + str(cells))
                        continue # skip bad rows

                # Parse cells, ignoring question mark columns, and add to cell_dict
                # Then pass cells dict to supplied function, fn
                cell_dict = {}
                i = 0
                for cell in cells:
                    # Check header for ignored columns
                    if first_line:
                        if ignoreCol(cell):
                            ignored_columns.append(i)
                            continue
                    # If cell is in ignored column, ignore it
                    elif i in ignored_columns:
                        continue
                    # Handle unknown (?) cell
                    if "?" in cell:
                        cell = None
                    else:  
                        cell = cell.strip()
                    cell_dict[i] = cell
                    i += 1

                fn(cell_dict)
                first_line = False
                
                

