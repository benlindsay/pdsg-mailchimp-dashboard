#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from flask import render_template, request, session, flash
from app import flaskapp
from app.plot import cum_signups
from bokeh.embed import components
from app.settings import  FLASK_USERNAME, FLASK_PASSWORD

@flaskapp.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # Determine the selected optiom
        current_signups_over_time_opt = request.args.get("signups_over_time_opt")
        if current_signups_over_time_opt is None:
            current_signups_over_time_opt = 'School'

        # Create the plot
        plot = cum_signups(split_opt=current_signups_over_time_opt)

        # Embed plot into HTML via Flask Render
        script, div = components(plot)
        return render_template("index.html", script=script, div=div,
                signups_over_time_opts=['School'],
                current_signups_over_time_opt=current_signups_over_time_opt)

@flaskapp.route('/login', methods=['POST'])
def do_admin_login():
    if ( request.form['password'] == FLASK_PASSWORD and
         request.form['username'] == FLASK_USERNAME ):
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()
