import sys
from tbl import Tbl
from tbl import Sym

print("The arguments are:", str(sys.argv))

table = Tbl();
table.fromCsv(sys.argv[1])
print(table.goals)
for i, col in table.cols["all"].items():
    col.summarize()
table.dom()

    



