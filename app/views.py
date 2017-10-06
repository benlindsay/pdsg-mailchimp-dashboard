#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from flask import render_template, request, session, flash
from app import flaskapp
from app.data import feature_names
from app.plot import create_figure
from bokeh.embed import components
from app.settings import (
        FLASK_USERNAME,
        FLASK_PASSWORD,
        MAILCHIMP_USERNAME,
        MAILCHIMP_SECRET_KEY
    )

@flaskapp.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Determine the selected feature
        current_feature_name = request.args.get("feature_name")
        if current_feature_name == None:
            current_feature_name = "Sepal Length"

        # Create the plot
        plot = create_figure(current_feature_name, 10)

        # Embed plot into HTML via Flask Render
        script, div = components(plot)
        return render_template("index.html", script=script, div=div,
                               feature_names=feature_names,
                               current_feature_name=current_feature_name)

@flaskapp.route('/login', methods=['POST'])
def do_admin_login():
    if ( request.form['password'] == FLASK_PASSWORD and
         request.form['username'] == FLASK_USERNAME ):
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()
