

# step 1: 

Open 4 terminals in this order:

## terminal 1:

```bash
make clean; make ui
```

## terminal 2:

```bash
make background
```

## terminal 3:

```bash
make provide_live_data
```

## terminal 4:

```bash
make met
```

# step 2:

Open a web browser to http://localhost:1044 and http://localhost:1033


# overview

```
+------------------------+  +---------------------------+ +--------------------------+
| display live data.html |  |  background: update state | | functions to query state |
+-------^----------------+  +-------+------------+---^--+ +-+----^---------+---------+
        |                           |            |   |      |    |         |
        |                           |            |   |      |    |         |
        |                           |            |   |      |    |         |
        |                           |         +--v---+------v----+--+      |
  +-----+-------------+             |         |  machine state.json |      |
  | provide live data |             |         +---------------------+      |
  | on port 1044.py   <----+        |                                      |
  +-------------------+    |   +----v---------+                            |
                           +---+ metrics.json <----------------------------+
                               +--------------+
```
