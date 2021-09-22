# Suppose this is foo.py.

print("before import")
import math

print("before functionA")
def functionA():
    # print("Function A")
    return "Function A"

print("before functionB")
def functionB():
    # print("Function B {}".format(math.sqrt(100)))
    return "Function B {}".format(math.sqrt(100))
    

def test_functionA():
    assert functionA() == "Function A", "Not as EXPECTED"

def test_functionB():
    resp = functionB()
    assert resp == "Function B 10.0", "Not as EXPECTED got {resp}"

print("before __name__ guard")
if __name__ == '__main__':
    test_functionA()
    test_functionB()
print("after __name__ guard")