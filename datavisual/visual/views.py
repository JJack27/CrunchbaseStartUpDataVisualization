from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    host = "104.155.161.154"
    return render(request, 'index.html', {'host': host})