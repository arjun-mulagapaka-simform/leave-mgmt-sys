from django.shortcuts import render
from .forms import *

def index_view(request):
    return render(request,"frontend/dashboard.html")

def login_view(request):
    return render(request,"frontend/login.html", {"form":EmployeeLoginForm()})

def leave_history_view(request):
    return render(request,"frontend/leavehistory.html")

def leave_view(request,pk):
    return render(request,"frontend/leavepage.html",{"id":pk})

def pending_leaves_view(request):
    return render(request,"frontend/pendingleaves.html")

def request_leave_view(request):
    return render(request,"frontend/requestleave.html",{"form":LeaveRequestForm()})