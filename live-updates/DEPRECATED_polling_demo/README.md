
The video [youtube:ZBM28ZPlin8](https://www.youtube.com/watch?v=ZBM28ZPlin8) distinguishes Short Polling vs Long Polling vs WebSockets.

# short polling
Of those three, short polling is what I need for this prototype.
An implementation of short polling is shown here: https://www.youtube.com/watch?v=E0UGGxd2DOo

## PHP
That demo relies on PHP and I don't want to incur the overhead of running a server for PHP rendering.

Interestingly, on a Mac, I can run
```bash
php viewcount.php
{"viewCount":1380}
```

## ZeroMQ

Instead of PHP providing JSON, I can use ZeroMQ to provide JSON

ZMQ's "ports" aren't the same as TCP ports.

# write-to-disk as API

A fourth option since my demo is entirely local would be to write state data to disk and then query those files on disk.

That avoids use of ports by leveraging a common file system.

However, modern browsers like Chrome disable that access.
The functionality can be re-enabled using
`--allow-file-access-from-files`
as per [https://stackoverflow.com/a/34579496/1164295](https://stackoverflow.com/a/34579496/1164295)

# irrelevant options

I don't need AJAX
[https://tyk.io/blog/moving-beyond-polling-to-async-apis/](https://tyk.io/blog/moving-beyond-polling-to-async-apis/)
