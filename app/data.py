#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

import pandas as pd
import numpy as np
import os.path as op
from app.settings import MAILCHIMP_USERNAME, MAILCHIMP_SECRET_KEY
from mailchimp3 import MailChimp

dir_path = op.dirname(op.realpath(__file__))
data_dir_path = op.join(dir_path, 'data')

iris_df = pd.read_csv(op.join(data_dir_path, 'iris.data'),
                      names=["Sepal Length", "Sepal Width", "Petal Length",
                             "Petal Width", "Species"]
                      )
feature_names = iris_df.columns[0:-1].values.tolist()

client = MailChimp(MAILCHIMP_USERNAME, MAILCHIMP_SECRET_KEY)
list_id = '1b1f4112db'

def create_df_questions():
    interest_categories = client.lists.interest_categories.all(
            list_id=list_id, get_all=True)
    question_ids = []
    question_titles = []
    for ic in interest_categories['categories']:
        question_ids.append(ic['id'])
        question_titles.append(ic['title'])
    df_questions = pd.DataFrame({'question_id': question_ids, 'question_title': question_titles}).set_index('question_id')
    school_qid, degree_qid = df_questions.index
    return df_questions

df_questions = create_df_questions()

def create_df_checkboxes(df_questions):
    checkbox_ids = []
    checkbox_names = []
    question_ids = []
    for qid in df_questions.index:
        interests = client.lists.interest_categories.interests.all(
                list_id=list_id, category_id=qid, get_all=True)
        for interest in interests['interests']:
            checkbox_ids.append(interest['id'])
            checkbox_names.append(interest['name'])
            question_ids.append(interest['category_id'])
    df_checkboxes = pd.DataFrame({
            'checkbox_id': checkbox_ids,
            'checkbox_name': checkbox_names,
            'question_id': question_ids}).set_index('checkbox_id')
    return df_checkboxes

df_checkboxes = create_df_checkboxes(df_questions)

def create_df_members():
    members = client.lists.members.all(list_id, get_all=True)
    member_dict_list = []
    for mem in members['members']:
        member_dict = {'member_id': mem['id'],
                       'name': mem['merge_fields']['FULLNAME'],
                       'email': mem['email_address'],
                       'email_type': mem['email_type'],
                       'status': mem['status'],
                       'timestamp_opt': mem['timestamp_opt'],
                       'timestamp_signup': mem['timestamp_signup']
                      }
        member_dict_list.append(member_dict)
    df_members = pd.DataFrame(member_dict_list).set_index('member_id')
    df_members['timestamp_opt'] = pd.to_datetime(df_members['timestamp_opt'])
    df_members['timestamp_signup'] = pd.to_datetime(
            df_members['timestamp_signup'])
    return df_members

df_members = create_df_members()

def create_df_true_checkboxes():
    members = client.lists.members.all(list_id, get_all=True)
    true_checkbox_dict_list = []
    for mem in members['members']:
        for key, val in mem['interests'].items():
            if val is True:
                true_checkbox_dict = {'member_id': mem['id'],
                                      'checkbox_id': key}
                true_checkbox_dict_list.append(true_checkbox_dict)
    df_true_checkboxes = pd.DataFrame(true_checkbox_dict_list)
    df_true_checkboxes = df_true_checkboxes.join(
            df_checkboxes[['question_id']], on='checkbox_id')
    return df_true_checkboxes

df_true_checkboxes = create_df_true_checkboxes()

school_qid, degree_qid = df_questions.index
df_school = df_true_checkboxes[
        df_true_checkboxes['question_id'] == school_qid
    ].drop('question_id', axis=1).copy()
df_school = df_school.rename(columns={'checkbox_id': 'school_id'})
df_degree = df_true_checkboxes[
        df_true_checkboxes['question_id'] == degree_qid
    ].drop('question_id', axis=1).copy()
df_degree = df_degree.rename(columns={'checkbox_id': 'degree_id'})

def create_df_school_and_degree(df_school, df_degree):
    df_school_and_degree = pd.merge(df_school, df_degree, on='member_id')
    df_school_and_degree = pd.merge(
            df_school_and_degree, df_checkboxes[['checkbox_name']],
            left_on='school_id', right_index=True
        ).rename(columns={'checkbox_name': 'school'})
    df_school_and_degree = pd.merge(
            df_school_and_degree, df_checkboxes[['checkbox_name']],
            left_on='degree_id', right_index=True
        ).rename(columns={'checkbox_name': 'degree'})
    df_school_and_degree['count'] = 1.0 / df_school_and_degree.groupby(
            'member_id')['member_id'].transform('count')
    return df_school_and_degree

df_school_and_degree = create_df_school_and_degree(df_school, df_degree)

def create_df_pivot(df_school_and_degree):
    df_pivot = pd.pivot_table(df_school_and_degree,
            index='school', columns='degree', values='count', aggfunc=np.sum
        ).fillna(0)
    deg_list = ['Bachelors', 'Masters', 'PhD', 'Postdoctoral', 'MD', 'Other']
    df_pivot = df_pivot[deg_list]
    schools_low_to_high = df_pivot.sum(axis=1).sort_values().index
    df_pivot = df_pivot.loc[schools_low_to_high]
    return df_pivot

df_pivot = create_df_pivot(df_school_and_degree)
