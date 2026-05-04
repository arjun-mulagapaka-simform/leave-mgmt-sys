from django.shortcuts import render
from .forms import *

def index_view(request):
    return render(request,"frontend/dashboard.html")

def login_view(request):
    return render(request,"frontend/login.html", {"form":EmployeeLoginForm()})