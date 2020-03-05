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
def get_counts(df, features, threshold, unknown):
    groups = df.groupby(features)['permalink']
    counts = groups.count()
    counts = counts[counts > threshold]
    print(unknown)
    if not unknown:
        counts = counts.drop("Unknown")
    return counts



class FilterAPI(APIView):

    def get(self, request,*args, **kwargs):
        # test query = http://127.0.0.1:8000/filter/?filter1=market&threshold1=500&filter2=founded_year&threshold2=1996&filter3=status&threshold3=None&label=count&unknown=True
        # Read filter values
        filters = {}
        filter_names = [self.request.query_params.get('filter1'),\
            self.request.query_params.get('filter2'),\
            self.request.query_params.get('filter3')]
        for i in range(len(filter_names)):
            filters[filter_names[i]] = {}
            try:
                filters[filter_names[i]]['threshold'] = float(self.request.query_params.get('threshold'+str(i+1)))
            except:
                filters[filter_names[i]]['threshold'] = 0
        
        # Read label values
        label_name = self.request.query_params.get('label') 
        label = {'label': label_name}

        # Read Unknown
        unknown = True if self.request.query_params.get("unknown") == 'True' else False 

        response = {"Result": "data"}

        # ===================
        # Testing code
        response = label

        for key in filters.keys():
            response[key] = filters[key]
        # End of testing
        # ====================

        # Get date from the data base
        path_of_data = './cleaned_data.csv'
        df = pd.read_csv(settings.DATA_FOLDER, encoding='unicode-escape')
        
        # generate tree structure of for data visualizing
        data = {'name':'root'}
        if label_name == 'count':
            children = get_counts(df, filter_names[0], filters[filter_names[0]]['threshold'], unknown)

        print(children)



        return Response(response, status = 200)