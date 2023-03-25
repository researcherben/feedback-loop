#!/usr/bin/env python3

"""

Given a functional relation 

                    +--<------------------------<--+
                    |                              |
        +----+     c|     +----+         +----+  c |
x ----->|    |      +---->|    |         |    +->--+
        | A  |  a         | B  |  b      | C  |
y ----->|    +----------->|    +-------->|    +-------> d
        +----+            +----+         +----+

What is the value of d as a function of (x,y)?

Graph created using https://asciiflow.com/#/

Whether d=f(x,y) converges depends on the initial value of c (as well as the functions A,B,C). 

TODO: generate the graph from Python functions

d = f(x,y) = 

"""

def A(int: x, int: y) -> int:
    """
    """
    a = x + y
    return a

def B(int: c, int: a) -> int:
    """
    """
    b = a + c
    return b

def C(int: b):
    """
    """
    c = b+1
    d = d+2
    return c,d

if __name__ == "__main__":


x = 4
y = 5

a = A(x,y)

initial_c = 2

b = B(initial_c, a)

c, d = C(b)

print("d =", d)

# EOF
