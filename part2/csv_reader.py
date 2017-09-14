
skipped_rows = []
header = True
ignored_columns = []
header_length = None

#Control Function
#################
# File extensions allowed - list
fext = ['txt', 'csv']
# Lines ends in comma - return boolean
def incompleteLine(txt):
    return txt[-1:] == ','

# If a col name includes "?" - return true
def ignoreCol(txt):
    return txt.find("?") == 0


#Row filtering
# ################
# check each line - remove padding, space chars, comments
#  replace it with "" string, check if non-empty row then
def cleanRow(txt):
    txt = txt.split('#')
    txt = txt[0].strip()
    return txt


#Iterator for each line
#########################
def withEachLine(fileName, fn):
    
    global header
    last_cells = []
    if (fileName.strip()[-3:] in fext for s in fext):
       with open(fileName, 'r') as f:

            for line in f:
               
                line = cleanRow(line) # remove comments and padding
                if len(line) == 0:
                    continue

                cells = line.split(",")
                if incompleteLine(line): #incomplete line - multi line record
                    last_cells = last_cells + cells[:-1]
                    continue
                if len(last_cells):
                    cells = last_cells + cells
                    last_cells = []

                # If header, set header length
                cell_dict = {}
                
                if header:
                    header_length = len(cells)
                else:
                    if len(cells) != header_length:
                        print("Error: incorrect number of cells. Line: " + str(line))
                        continue

                # Now we have a full data line
                
                i = 0
                for cell in cells:
                    if header:
                        if ignoreCol(cell):
                            ignored_columns.append(i)
                            continue
                    elif i in ignored_columns:
                        continue
                    if "?" in cell:
                        cell = None
                    cell_dict[i] = cell
                    i += 1
                print(cell_dict)
                fn(cell_dict)

                header = False
                
                

