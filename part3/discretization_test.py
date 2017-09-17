import sys
sys.path.insert(0, '../part2')
import tbl
from discretization import Range
from discretization import Super


table = tbl.Tbl();
table.fromCsv("../part2/auto.csv")

# TODO: Should this login be a part of something? Tbl? Range?
# (Maybe not, it might need to be flexible for testing)
colIndex = 2
values = []
for r in table.rows:
    row = table.rows[r]
    value = row.cells[colIndex]
    if value is not None:
        values.append(value)

range = Range()
range.get_ranges(values)

