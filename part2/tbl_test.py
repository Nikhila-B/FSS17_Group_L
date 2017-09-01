from tbl import Tbl
from tbl import Sym

table = Tbl();
table.update(5)

sym = Sym();

sym.update("hello")
sym.summarize()
print()

sym.update("whoa")
sym.summarize()
print()

sym.update("hi")
sym.summarize()
print()

sym.update("whoa")
sym.summarize()
print()

print(sym.distance(None, None))
print(sym.distance("hi", None))
print(sym.distance(None, "hello"))
print(sym.distance("hi", "hi"))
print(sym.distance("hi", "hello"))


print()
sym.ent()
sym.summarize()




