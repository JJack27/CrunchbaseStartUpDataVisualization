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

class FilterAPI(APIView):

    def get(self, request,*args, **kwargs):
        # test query = http://127.0.0.1:8000/filter/?filter1=sd&value1=a&filter2=sa&value2=asdf&filter3=sdoiioj&value3=sdfajior34&label=asdfijoejfwe&value_label=adfsfjie
        # Read filter values
        filters = {}
        filter_names = [self.request.query_params.get('filter1'),\
            self.request.query_params.get('filter2'),\
            self.request.query_params.get('filter3')]
        filters[filter_names[0]] = self.request.query_params.get('value1')
        filters[filter_names[1]] = self.request.query_params.get('value2')
        filters[filter_names[2]] = self.request.query_params.get('value3')
        
        # Read label values
        label_name = 'label'+self.request.query_params.get('label') 
        label = {label_name: self.request.query_params.get('value_label')}

        # Read Unknown
        unknown = bool(self.request.query_params.get('unknown'))

        response = {"Result": "data"}

        # ===================
        # Testing code
        response = {label_name: label[label_name]}

        for key in filters.keys():
            response[key] = filters[key]
        # End of testing
        # ====================

        # Get date from the data base
        path_of_data = '../data/investments.csv'

        layer1 = {}
        layer2 = {}
        layer3 = {}




        return Response(response, status = 200)