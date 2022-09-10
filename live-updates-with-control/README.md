

terminal 1:

```bash
make clean; make ui
```

# terminal 2:

```bash
make background
```

# terminal 3:

```bash
make provide_live_data
```

# terminal 4:

```bash
make met
```




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
