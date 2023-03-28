
# feedback loops: overview

I can represent the function `a = A(x)` visually as
```
        +---+
x ----->| A +----> a
        +---+
```

If the input of one function is  the output of another, the graph
```
        +---+  a  +---+
x ----->| A +---->| B +----> b
        +---+     +---+
```
represents the pair of equations `a = A(x)` and `b = B(a)`.

A third configuration can be created by introducing a new function, `a = D(x,b)`:

```
          +---+     +---+
x ------->|   |     |   |
          |   | a   |   |
      +-->| D +---->| B +-+--> b
      |   +---+     +---+ |
      |                   |
      |         b         V
      +-<------------<----+
```
This is now an interdependent set of equations:
```
a = D(x,b)
b = B(a)
```
I can't evaluate `D` without knowing `b`, and I can't evaluate `B` without knowing `a`.

To break this stalemate, I introduce a new variable, `b_{initial}`. 
Let `b = b_{initial}` when I first evaluate `D`, and then use the result of `B` to compute `D` again.

The consequence of this feedback loop is that, in the formula `b = F(x, b_{initial})`, 
* `b` could converge to a steady-state value for `b` after many iterations of the loop
* `b` could oscillate (and thus not converge)
* `b` could be chaotic if `D` or `B` are non-linear

# feedback loops: multiple

A single feedback loop is the simplest set of interdependent equations.

A slightly more complicated graph is
```
                       +--------------------------------+
                       |                c               |
           +----+     c|     +-----+         +-----+    |c
x -------->|    |      +---->|     |         |     +----+
           | A  |  a         | B   |    b    | C   |   
     +---->|    +----------->|     +---+---->|     +------------> d
     ^     +----+            +-----+   |     +-----+
    m|                                 |
     |        m   +-----+     b        V
     +-------<----|  M  |<-------------+
                  +-----+

```

The over-arching equation is `d = F(x)`, and the loops are
`c,b` and `b,m,a`.
Because `b` is present in both loops, only `b` needs to be initialized.

When there are multiple loops and the loops share no common variables,
then one parameter from each loop needs to be initialized.
```
               +---+      a        +---+
x ------------>| A +-------------->| B +-----------> b
               |   |               |   |
           +-->|   +----+       +->|   +--+
          c|   +---+    |e      |  +---+  |d
           |            |       |         |
           |   +---+    |      g|  +---+  |
           +---+ C |<---+       +--+ D |<-+
               +---+               +---+
```
Multiple initializations are required. 
The loops are `c,e` and `d,g`. 
One variable from each loop needs to be initialized. 
The four choices are `c,g`, `c,d`, `e,g`, or `e,d`.


# References

<https://en.wikibooks.org/wiki/Control_Systems/Feedback_Loops>


After creating this model, I found a related reference

```
title={Mathematical modeling of interdependent infrastructure: An object-oriented approach for generalized network-system analysis},
author={Neetesh Sharma, Paolo Gardoni},
doi={https://doi.org/10.1016/j.ress.2021.108042},
journal={Reliability Engineering & System Safety},
volume={217},
month={January},
year={2022},
url={https://www.sciencedirect.com/science/article/abs/pii/S0951832021005470}
```
