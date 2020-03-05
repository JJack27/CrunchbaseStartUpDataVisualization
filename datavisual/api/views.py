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
def get_counts(df, filters, unknown):

    filtered_data = df.copy()
    
    equal_filter_cols = ['category_list', 'homepage_url', 'status', \
        'country_code', 'region', 'city', 'founded_at',  'state_code']
    if not unknown:
        for key in filters.keys():
            if key in equal_filter_cols or key == 'market':
                filtered_data = filtered_data[filtered_data[key] != 'Unknown']
            else:
                filtered_data = filtered_data[filtered_data[key] != 0]
    
    for fil, threshold in filters.items():
        if fil == "market":
            filtered_data = filtered_data[filtered_data['market_count'] > threshold]
        elif fil in equal_filter_cols:
            if threshold != 'None':
                filtered_data = filtered_data[filtered_data['market_count'] == threshold]
        else:
            filtered_data = filtered_data[filtered_data[fil] > threshold]

    groups = filtered_data.groupby(list(filters.keys()))['market']
    counts = groups.count()

    
    return counts

def generate_tree(data):
    # first generate index
    label = data.index.labels
    levels = data.index.levels
    keys = [] 
    for i in range(len(label[0])):
        keys.append([levels[0][label[0][i]],levels[1][label[1][i]],levels[2][label[2][i]]])
    #for key in keys:
    #    print(key)
    '''
    tree = {'name': 'Root', 'children':[], 'children_names':[]}
    for key in keys:
        if key[0] not in tree['children_names']:
            tree['children_names'].append(key[0])
            tree['children'].append({'name': key[0], 'children':[], 'children_name':[]})

        if key[1] not in tree[key[0]]['children_names']:
            tree[key[0]]['children_names'].append(key[1])
            for child in tree['children']:
                if child['name'] == key[1]:
                    child['children'].append({'name': key[1], 'children':[], 'children_name':[]})

        if key[1] not in tree[key[0]][]:
            tree[key[0]]['children_names'].append(key[1])
            tree[key[0]]['children'].append({'name': key[1], 'children':[], 'children_name':[]})
    '''
    tree = {}
    for key in keys:
        if key[0] not in tree.keys():
            tree[key[0]] = {'name':key[0]}
            
        if key[1] not in tree[key[0]].keys():
            tree[key[0]][key[1]] = {'name':key[1]}
        
        if key[2] not in tree[key[0]][key[1]].keys():
            tree[key[0]][key[1]][key[2]] = {'name': key[2], 'value':data[key[0]][key[1]][key[2]]}#, 'value':data[key[0]][key[1]][key[2]]
    
    re_tree = {'name': 'Root', 'children': [], 'children_names':[]}
    
    for key in tree.keys():
        child_dic1 = {'name':key, 'children':[], 'children_names':[]}
        if tree[key]['name'] not in re_tree['children_names']:
            re_tree['children_names'].append(key)
            re_tree['children'].append(child_dic1)
        
        for key2 in tree[key].keys():
            if key2 == 'name':
                continue
            child_dic2 = {'name':key2, 'children':[], 'children_names':[]}
            if key2 not in child_dic1['children_names']:
                child_dic1['children_names'].append(key2)
                child_dic1['children'].append(child_dic2)

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
        path_of_data = './cleaned_data.csv'
        df = pd.read_csv(settings.DATA_DIR, encoding='unicode-escape')
        
        # generate tree structure of for data visualizing
        data = {'name':'root'}
        if label_name == 'count':
            children = get_counts(df, filters, unknown)

        #print(children.index)
        tree = generate_tree(children)
        response['tree'] = tree
        return Response(response, status = 200)