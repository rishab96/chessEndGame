[syzygy-tables.info](https://syzygy-tables.info)
================================================

User interface and public API for probing Syzygy endgame tablebases.

[![Screenshot of the longest winning 6 piece endgame](/screenshot.png)](https://syzygy-tables.info/?fen=6N1/5KR1/2n5/8/8/8/2n5/1k6%20w%20-%20-%200%201)

Running
-------

Dependencies:

    pip install flask
    pip install python-chess
    pip install tornado # Required for dealing with many
                        # open file descriptors
                        # when serving six-men tablebases.
    pip install htmlmin # Recommended.

    npm install -g grunt-cli
    npm install

Create combined JavaScript and CSS files using Grunt:

    grunt

Start the server on port 5000:

    python server.py

Syzygy tablebase files
----------------------

Only the small four-men tablebases are in this Git repository. Optionally [generate](https://github.com/syzygy1/tb) or [download](http://oics.olympuschess.com/tracker/index.php) five-men and six-men tablebases and place them in the corresponding directories.

Gaviota tablebases
------------------

Optionally build and install [libgtb](https://github.com/michiguel/Gaviota-Tablebases) and [download](http://www.olympuschess.com/egtb/gaviota/filelist.txt) Gaviota tablebase files. Put them into the `gaviota` directory.

API
---

See [https://syzygy-tables.info/apidoc](https://syzygy-tables.info/apidoc?fen=4k3/8/8/8/8/8/8/4K3%20w%20-%20-%200%201) for information about the JSON API.

Hacking
-------

Have a look at `server.py` for server side code. The client side code is in
`static/js/client.js`.

License
-------

This project is licensed under the GPLv3 with the following dependencies:

* [python-chess](https://github.com/niklasf/python-chess) ([GPL3](https://github.com/niklasf/python-chess/blob/master/LICENSE))
* [chessboard.js](http://chessboardjs.com/) ([MIT](https://github.com/oakmac/chessboardjs/blob/master/LICENSE))
* [chess.js](https://github.com/jhlywa/chess.js) ([MIT](https://github.com/jhlywa/chess.js/blob/master/LICENSE))
* [Bootstrap](http://getbootstrap.com/) ([MIT](https://github.com/twbs/bootstrap/blob/master/LICENSE))
* [jQuery](https://jquery.com/) ([MIT](https://github.com/jquery/jquery/blob/master/LICENSE.txt))
* [Flask](http://flask.pocoo.org/) ([BSD](http://flask.pocoo.org/docs/0.10/license/">BSD</a>))
* [htmlmin](https://htmlmin.readthedocs.org/en/latest/) ([BSD](https://github.com/mankyd/htmlmin/blob/master/LICENSE))
* [Tornado](http://www.tornadoweb.org/en/stable/) ([Apache License Version 2.0](https://github.com/tornadoweb/tornado/blob/master/LICENSE))

Thanks to all of them and special thanks to Ronald de Man for [his endgame tablebases](https://github.com/syzygy1/tb)!
