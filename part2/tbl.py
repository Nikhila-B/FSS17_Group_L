
class Tbl:

    def __init__(self):
        # init instance vars

    # Read in CSV file, call update on every row
    # Make sure handles multiple lines
    def fromCsv(fileName):

    # Update the table with a row
    # Calls header for first row, data for rest
    def update(cells):

    # Create headers from first row of table
    # Hmmm... not sure about the pairs part -- read docs
    # Calls categories to get spec for the column
    def header(cells):

    # Looks for special characters in the header text and returns spec for the special character
    # headerTxt - column header text to parse
    def categories(headerTxt):

    # Create new Row and update
    # In lua, something called old for (I think) updating rows. Don't worry about it for now.
    def data(cells):



class Row:
    
    def __init__(self):
        # Initialize id and cells[]

    # Update the table headers
    def update(cells, table):

    # Calculate distance between two rows
    # Or static function? Can you do that in python?
    def distance(otherRow):

    # Get domination score for row, by comparing all pairs of row
    # Use passed funtion or if none passed, domination1 (assume dom1 for now)
    def dominate():

    # i.e. dominate1
    # subrouting of dominate that determines if this row dominates otherRow
    # Or.. static?
    def dominationCompare(otherRow):
        
#TODO fill out
class Num:

    def __init__(self):
        #self.data = []

#TODO fill out
class Sym:

    def __init__(self):
        #self.data = []
    
