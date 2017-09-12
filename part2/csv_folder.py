import sys
print("This is the name of the script: ", sys.argv[0])
print("Number of arguments:", len(sys.argv))
print("The arguments are:", str(sys.argv))

approved_cols = []
num_cols = []
num_dic = {}
sym_cols = []
row_list= []
skipped_rows = []
header = True
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

#Column filtering
##################
# Using the helper function - to check if col not ignored
# and convert to number if needed and return out
def cellsNotIgnoring(line, row_index):
    out =[]
    col = 0
    #line = cleanRow(line)
    line = line.split(',')

   
    if header == True:
        for i=0, word in line:
            word = word.strip()
            ignore_col = ignoreCol(word)
            if(not ignore_col):
                magic_char = word[0]
                if magic_char == '$':
                    num_dic = {i: 0}
                elif magic_char == '<':
                    num_dic = {i, -1}
                elif magic_char == '>':
                    num_dic = {i, 1}
                else:
                    sym_cols.append(i)
                    approved_cols.append(i)

        #Now add the  numeric cols to approved cols:
        approved_cols.append(num_dic.keys())
    
    else:
        #print("OKAY non header now") # check for num of cells here 
        #print(" convert between num and sym") # throw error for conversion here
        row = []
        for c in approved_columns:
            cell = line[c]
            if c in num_columns: # Convert numeric cells to float
                try:
                    cell = float(cell)
                except ValueError:
                    print("ERROR: Row " + str(row_index) + " has an invalid numeric cell " + str(c))
                    skipped_rows.append(row_index)
                    return
            row.append(cell)
    
         row_list.append(row)
        

#Iterator for each line
#########################
def WithEachLine(fileName):
    last_line = []
    if (fileName.strip()[-3:] in fext for s in fext):
       with open(fileName, 'r') as f:
            results=[]
            i = 0;
            for line in f:
                if(i!=0):
                    header = False
                i = i + 1
                line = cleanRow(line) # remove comments and padding
                if(not incompleteLine(line) and len(line)>0): # not incomplete/blank
                        cellsNotIgnoring(line, i)
                elif(len(line)>0 and incompleteLine(line)): #incomplete line - multi line record
                    last_line = last_line + line[1:]
                    continue
                if len(last_line):
                    line = last_line + line
                    last_line = []

WithEachLine(sys.argv[1])