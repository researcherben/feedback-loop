#!/usr/bin/env python3

"""

Given a functional relation 

                    +--<------------------------<--+
                    |                              |
                   c|     +----+         +----+  c |
                    +---->|    |         |    +->--+
                          | B  |  b      | C  |
                a ------->|    +-------->|    +-------> d
                          +----+         +----+

What is the value of d as a function of a?

Graph created using https://asciiflow.com/#/

Whether d=f(a) converges depends on the initial value of c (as well as the functions B,C). 

TODO: generate the graph from Python functions

"""


def B(c: int, a: int) -> int:
    """
    """
    b = a + c
    return b

def C(b: int):
    """
    """
    c = b+1
    d = b+2
    return c,d

if __name__ == "__main__":

    a = 4
    initial_c = 2

    c = initial_c
    number_of_iterations = 10

    results = []
    for iteration_index in range(number_of_iterations):
        b = B(c, a)
        c, d = C(b)
        this_loop_dict = {'index': iteration_index,
                          'a': a,
                          'b': b,
                          'c': c,
                          'd': d}
        results.append(this_loop_dict)

    print(results)

# EOF
