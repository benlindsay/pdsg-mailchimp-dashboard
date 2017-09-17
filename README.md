# flask-bokeh-template

A simple Flask template that supports Bokeh plots

## Getting Started

You probably want to create a fresh virtual environment. I like using Conda. If we want to put this upon Heroku eventually, it looks like the latest Python version they support is 3.4.1, so:

```
$ conda create -n mynewenv python=3.4.1
$ . activate mynewenv
(mynewenv) $ cd /path/to/flask-bokeh-template
(mynewenv) $ pip install -r requirements.txt
```

If you already have an environment for this but the `requirements.txt` file has changed, do all of those commands except the first.

Then run the app with

```
(mynewenv) $ ./run.py
```
