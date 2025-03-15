from flatliner import Flatliner

a = Flatliner()
a.set_ast("test_inputs/loops.py")
result = a.unparse()
print(result)