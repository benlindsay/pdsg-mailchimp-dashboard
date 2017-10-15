#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.plotting import figure, show
from bokeh.palettes import Category20
from app.data import df_members, df_school_and_degree, df_pivot
import pandas as pd
import numpy as np

# Create the main plot
def cum_signups(split_opt='School'):
    if split_opt == 'School':
        df_bk_school = ( df_members
                         [
                           ~df_members['timestamp_signup'].isnull()
                         ]
                         .copy()
                       )
        features = ['member_id', 'school', 'degree', 'count']
        df_bk_school = ( df_school_and_degree[features]
                         .join(df_bk_school, how='inner', on='member_id')
                       )
        df_bk_school = df_bk_school.sort_values('timestamp_signup')
        def f(x):
             return pd.Series(
                     {'degree_str': ', '.join(x['degree']),
                      'name': x['name'].iloc[0],
                      'timestamp_signup': x['timestamp_signup'].iloc[0],
                      'email': x['email'].iloc[0],
                      'count': x['count'].sum()})
        df_bk_school = ( df_bk_school
                         .groupby(['member_id', 'school'])
                         .apply(f)
                         .reset_index()
                       )
        df_bk_school['school_str'] = ( df_bk_school
                                       .groupby('member_id')['school']
                                       .transform(lambda x: ', '.join(x))
                                     )
        df_bk_school['date_str'] = ( df_bk_school['timestamp_signup']
                                     .map(lambda x: x.strftime('%m/%d'))
                                   )
        df_bk_school = df_bk_school.sort_values('timestamp_signup')
        name_by_nth = pd.DataFrame({'name': df_bk_school['name'].unique()})
        name_by_nth['nth_to_join'] = name_by_nth.index + 1
        name_by_nth = name_by_nth.set_index('name')
        df_bk_school = df_bk_school.join(name_by_nth, on='name')
        p = figure(x_axis_type='datetime', y_axis_label='Number of Signups',
                   plot_width=900, plot_height=500,
                   sizing_mode='scale_width',
                   tools="pan,wheel_zoom,box_zoom,box_select,save,reset",
                   toolbar_location='left', toolbar_sticky=False)
        items_list = []
        schools_low_to_high = list(df_pivot.index)
        colors = Category20[len(schools_low_to_high)]
        for i, school in enumerate(reversed(schools_low_to_high)):
            s_group = df_bk_school[df_bk_school['school'] == school].copy()
            s_group['cum_count'] = np.cumsum(s_group['count'])
            source = ColumnDataSource(data=s_group)
            r_line = p.line('timestamp_signup', 'cum_count', source=source,
                            color=colors[i], line_width=2)
            r_circle = p.circle('timestamp_signup', 'cum_count', source=source,
                                color=colors[i], size=5)
            items_list.append((school, [r_line, r_circle]))
            p.add_tools(HoverTool(renderers=[r_circle],
                                  tooltips="""
                                      <div style="word-wrap: break-word;
                                                  max-width: 200px;">
                                          <h3>@name</h3>
                                          <p>@email</p>
                                          <p>@school_str</p>
                                          <p>@degree_str</p>
                                          <p>Signed up @date_str</p>
                                          <p># @cum_count to join from {}</p>
                                          <p># @nth_to_join to join overall</p>
                                      </div>
                                      """.format(school)
                                 )
                       )
        legend = Legend(items=items_list)
        p.add_layout(legend, 'right')
    elif split_opt == 'Degree':
        df_bk_degree = ( df_members
                         [
                           ~df_members['timestamp_signup'].isnull()
                         ]
                         .copy()
                       )
        features = ['member_id', 'school', 'degree', 'count']
        df_bk_degree = ( df_school_and_degree[features]
                         .join(df_bk_degree, how='inner', on='member_id')
                       )
        df_bk_degree = df_bk_degree.sort_values('timestamp_signup')
        def f(x):
             return pd.Series(
                     {'school_str': ', '.join(x['school']),
                      'name': x['name'].iloc[0],
                      'timestamp_signup': x['timestamp_signup'].iloc[0],
                      'email': x['email'].iloc[0],
                      'count': x['count'].sum()})
        df_bk_degree = ( df_bk_degree
                         .groupby(['member_id', 'degree'])
                         .apply(f)
                         .reset_index()
                       )
        df_bk_degree['degree_str'] = ( df_bk_degree
                                       .groupby('member_id')['degree']
                                       .transform(lambda x: ', '.join(x))
                                     )
        df_bk_degree['date_str'] = ( df_bk_degree['timestamp_signup']
                                     .map(lambda x: x.strftime('%m/%d'))
                                   )
        df_bk_degree = df_bk_degree.sort_values('timestamp_signup')
        name_by_nth = pd.DataFrame({'name': df_bk_degree['name'].unique()})
        name_by_nth['nth_to_join'] = name_by_nth.index + 1
        name_by_nth = name_by_nth.set_index('name')
        df_bk_degree = df_bk_degree.join(name_by_nth, on='name')
        p = figure(x_axis_type='datetime', y_axis_label='Number of Signups',
                   plot_width=900, plot_height=500,
                   sizing_mode='scale_width',
                   tools="pan,wheel_zoom,box_zoom,box_select,save,reset",
                   toolbar_location='left', toolbar_sticky=False)
        items_list = []
        degrees_low_to_high = list(df_pivot.columns)
        colors = Category20[len(degrees_low_to_high)]
        for i, degree in enumerate(reversed(degrees_low_to_high)):
            s_group = df_bk_degree[df_bk_degree['degree'] == degree].copy()
            s_group['cum_count'] = np.cumsum(s_group['count'])
            source = ColumnDataSource(data=s_group)
            r_line = p.line('timestamp_signup', 'cum_count', source=source,
                            color=colors[i], line_width=2)
            r_circle = p.circle('timestamp_signup', 'cum_count', source=source,
                                color=colors[i], size=5)
            items_list.append((degree, [r_line, r_circle]))
            p.add_tools(HoverTool(renderers=[r_circle],
                                  tooltips="""
                                      <div style="word-wrap: break-word;
                                                  max-width: 200px;">
                                          <h3>@name</h3>
                                          <p>@email</p>
                                          <p>@school_str</p>
                                          <p>@degree_str</p>
                                          <p>Signed up @date_str</p>
                                          <p># @cum_count to join from {}</p>
                                          <p># @nth_to_join to join overall</p>
                                      </div>
                                      """.format(degree)
                                 )
                       )
        legend = Legend(items=items_list)
        p.add_layout(legend, 'right')
    return p
