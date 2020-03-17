from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    host = "cunch.herokuapp.com"
    return render(request, 'index.html', {'host': host})