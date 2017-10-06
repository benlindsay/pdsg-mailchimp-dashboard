#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from app import flaskapp
import os

if __name__ == '__main__':
    flaskapp.secret_key = os.urandom(12)
    flaskapp.run(debug=True)
