from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    host = "http://localhost:8000"
    return render(request, 'index.html', {'host': host})