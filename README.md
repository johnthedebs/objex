# Objex

`objex` was created because I needed a way to quickly find out what a
given object was and what it could do. In the longer-term, I'd like it
to be an awesome interactive programming tool for Python.

The original goal was to pass `objex` an object which would cause it to
pause the Python interpreter, serving up a web page that allowed you
to poke around the given object. I still need to do a ton of work on
providing a clean way to do this but a proof-of-concept is provided in
`browser_test.py`.

The easiest way to get started is:

    git clone git://github.com/johnthedebs/objex.git
    mkvirtualenv objex && pip install -r requirements.txt
    python objex/browser_test.py

This launches a little Bottle server at http://localhost:8001 that gets
a bunch of info out of a simple and very contrived Cat class. Play
around! And if you can make it better (I'm sure you can) please send me
pull requests.
