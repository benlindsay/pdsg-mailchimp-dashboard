#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from flask import Flask
import pandas as pd

app = Flask(__name__)

from app import data
from app import views
