#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from flask import Flask
import pandas as pd

flaskapp = Flask(__name__)

from app import data
from app import views
from app import settings
