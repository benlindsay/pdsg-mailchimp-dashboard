#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from app import flaskapp
import os

flaskapp.secret_key = os.urandom(12)

if __name__ == '__main__':
    flaskapp.run(debug=True)
