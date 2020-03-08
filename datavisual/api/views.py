import datetime
import json
from django.db.models import F
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View, generic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.http import JsonResponse

import numpy as np 
import pandas as pd 

import requests

from django.conf import settings

# return a data frame of selected features and counts
def get_counts(df, filters, unknown, metric):

    filtered_data = df.copy()
    
    equal_filter_cols = ['category_list', 'homepage_url', 'status', \
        'country_code', 'region', 'city', 'founded_at',  'state_code']

    # remove unknown from the dataset if applicable
    if not unknown:
        for key in filters.keys():
            if key in equal_filter_cols or key == 'market':
                filtered_data = filtered_data[filtered_data[key] != 'Unknown']
            else:
                filtered_data = filtered_data[filtered_data[key] != 0]
    
    # retrieve data from the dataset based on given filter
    for fil, threshold in filters.items():
        if fil == "market":
            filtered_data = filtered_data[filtered_data['market_count'] > threshold]
        elif fil in equal_filter_cols:
            if threshold != 'None':
                filtered_data = filtered_data[filtered_data['market_count'] == threshold]
        else:
            filtered_data = filtered_data[filtered_data[fil] > threshold]

    # return based on metric
    if (metric == 'count'):
        groups = filtered_data.groupby(list(filters.keys()))['market']
        result = groups.count()
    else:
        groups = filtered_data.groupby(list(filters.keys()))['funding_total_usd']
        result = groups.sum()
    return result

# Given node of a tree, return the sum of values of the sub-tree
def sum_of_subtree(root):
    if 'value' in root.keys():
        return root['value']
    summation = 0
    for key in root.keys():
        if key == 'name':
            continue
        summation += sum_of_subtree(root[key])
    return summation

def generate_tree(data):
    # first generate index
    label = data.index.labels
    levels = data.index.levels
    index_names = data.index.names
    
    # declare helper variables
    columns_to_fill_na_unknown = ['market', 'category_list', 'homepage_url', 'status', \
        'country_code', 'region', 'city', 'founded_at',  'state_code']
    columns_to_fill_na_zero = ['founded_year']

    # Merge index to keys
    keys = [] 
    for i in range(len(label[0])):
        keys.append([levels[0][label[0][i]],levels[1][label[1][i]],levels[2][label[2][i]]])
    
    # Constructing intermediate tree for easily formatting
    tree = {}
    for key in keys:
        # first layer
        if key[0] not in tree.keys():
            tree[key[0]] = {'name':key[0]}
           
        # second layer
        if key[1] not in tree[key[0]].keys():
            tree[key[0]][key[1]] = {'name':key[1]}
        
        # third layer
        if key[2] not in tree[key[0]][key[1]].keys():
            tree[key[0]][key[1]][key[2]] = {'name': key[2], 'value':data[key[0]][key[1]][key[2]]}#, 'value':data[key[0]][key[1]][key[2]]
    
    # Constructing tree to return
    re_tree = {'name': 'Root', 'children': [], 'children_names':[]}
    for key in tree.keys():
        # first layer
        child_dic1 = {'name':key, 'children':[], 'children_names':[]}
        if tree[key]['name'] not in re_tree['children_names']:
            # directly set value of unknown
            if (key == 'Unknown' and index_names[0] in columns_to_fill_na_unknown) or (key == 0 and index_names[0] in columns_to_fill_na_zero):
                value_of_unknown = sum_of_subtree(tree[key])
                re_tree['children'].append({'name':'Unknown', 'value':value_of_unknown})
            else:
                re_tree['children_names'].append(key)
                re_tree['children'].append(child_dic1)
        
        # Second layer
        for key2 in tree[key].keys():
            if key2 == 'name':
                continue
            child_dic2 = {'name':key2, 'children':[], 'children_names':[]}
            if key2 not in child_dic1['children_names']:
                # Directly set value of unknown
                if (key2 == 'Unknown' and index_names[1] in columns_to_fill_na_unknown) or (key2 == 0 and index_names[1] in columns_to_fill_na_zero):
                    value_of_unknown = sum_of_subtree(tree[key][key2])
                    child_dic1['children'].append({'name':'Unknown', 'value':value_of_unknown})    
                else:
                    child_dic1['children_names'].append(key2)
                    child_dic1['children'].append(child_dic2)

            # Third layer
            for key3 in tree[key][key2].keys():
                if key3 == 'name':
                    continue
                child_dic3 = {'name':key3, 'value': tree[key][key2][key3]['value']}
                if key3 not in child_dic2['children_names']:
                    child_dic2['children_names'].append(key3)
                    child_dic2['children'].append(child_dic3)
    return re_tree




class FilterAPI(APIView):

    def get(self, request,*args, **kwargs):
        # test query = http://127.0.0.1:8000/filter/?filter1=market&threshold1=500&filter2=founded_year&threshold2=2008&filter3=status&threshold3=None&label=count&unknown=False
        # Read filter values
        filters = {}
        filter_names = [self.request.query_params.get('filter1'),\
            self.request.query_params.get('filter2'),\
            self.request.query_params.get('filter3')]
        for i in range(len(filter_names)):
            try:
                filters[filter_names[i]] = float(self.request.query_params.get('threshold'+str(i+1)))
            except:
                filters[filter_names[i]] = self.request.query_params.get('threshold'+str(i+1))
        
        # Read label values
        label_name = self.request.query_params.get('label') 
        label = {'label': label_name}

        # Read Unknown
        unknown = True if self.request.query_params.get("unknown") == 'True' else False 
        response = {"Result": "data"}

        # Get date from the data base
        df = pd.read_csv(settings.DATA_DIR, encoding='unicode-escape')
        
        # generate tree structure of for data visualizing
        children = get_counts(df, filters, unknown, label)
        print(children)

        tree = generate_tree(children)
        response['tree'] = tree
        return Response(response, status = 200)