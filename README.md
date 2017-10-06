# pdsg-mailchimp-dashboard

An interactive dashboard made with Flask and Bokeh. This is the source code for [http://pdsg-mailchimp-dashboard.herokuapp.com](http://pdsg-mailchimp-dashboard.herokuapp.com).

## Running locally

You probably want to create a fresh virtual environment. I like using `conda`, but you can use `virtualenv` as well.

```
$ conda create -n mynewenv python=3.6.2
$ . activate mynewenv
(mynewenv) $ cd /path/to/pdsg-mailchimp-dashboard
(mynewenv) $ pip install -r requirements.txt
```

If you already have an environment for this but the `requirements.txt` file has changed, do all of those commands except the first.

Then run the app with

```
(mynewenv) $ ./run.py
```
