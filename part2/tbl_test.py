from tbl import Tbl
from tbl import Sym

table = Tbl();
table.fromCsv("not used yet")
for i, col in table.cols["all"].items():
    col.summarize()

    



