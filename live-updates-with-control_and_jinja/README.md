Revised:
* single background process enabled by use of counters
* single "provide live data" server
* single UI server
* use of Jinja templates; see https://zetcode.com/python/jinja/ for tutorial

# HTTPS

* https://blog.anvileight.com/posts/simple-python-http-server/
* https://stackoverflow.com/questions/19705785/python-3-simple-https-server

# to address deadlock of `GET` calling a function that calls `PUT`
import asyncio


#https://docs.python.org/3/library/asyncio-subprocess.html
#https://realpython.com/async-io-python/


# FQDN causing slow load on Mac OSX

I tried disabling DNS lookups in Python

```python
# Disable logging DNS lookups
# https://stackoverflow.com/a/6761844/1164295
def address_string(self):
    # https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.client_address
    return str(self.client_address[0])
```

```python
# https://stackoverflow.com/a/5273870/1164295
# https://bugs.python.org/issue6085
def address_string(self):
    host, port = self.client_address[:2]
    #return socket.getfqdn(host)
    return host
```

https://stackoverflow.com/a/53143006/1164295
```bash
$ sudo scutil --get HostName
HostName: not set
$ hostname
Bens-MacBook-Air.local
$ sudo scutil --set HostName `hostname`
```

## step 1:

Open 3 terminals in this order:

### terminal 1:

```bash
make clean; make webserver_port1033.py
```

### terminal 2:

```bash
make background_process_to_update_state_and_metrics.py
```

## terminal 3:

```bash
make webserver_logging_port1044.py
```

## step 2:

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
