import sys
from tbl import Tbl

table = Tbl();
table.fromCsv(sys.argv[1])
for i, col in table.cols["all"].items():
    col.summarize()
    
table.dom()

    



