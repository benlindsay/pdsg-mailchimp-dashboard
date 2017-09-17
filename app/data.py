#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

import pandas as pd
import os.path as op
dir_path = op.dirname(op.realpath(__file__))
data_dir_path = op.join(dir_path, 'data')

iris_df = pd.read_csv(op.join(data_dir_path, 'iris.data'),
                      names=["Sepal Length", "Sepal Width", "Petal Length",
                             "Petal Width", "Species"]
                      )
feature_names = iris_df.columns[0:-1].values.tolist()
