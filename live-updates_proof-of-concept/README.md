

terminal 1:

```bash
background_process_to_update_state_and_metrics.py
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
https://asciiflow.com/#/
