#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from bokeh.charts import Histogram
from app.data import iris_df

# Create the main plot
def create_figure(current_feature_name, bins):
    p = Histogram(iris_df, current_feature_name,
                  title=current_feature_name, color='Species',
                  bins=bins, legend='top_right', width=600, height=400)

    # Set the x axis label
    p.xaxis.axis_label = current_feature_name

    # Set the y axis label
    p.yaxis.axis_label = 'Count'
    return p
