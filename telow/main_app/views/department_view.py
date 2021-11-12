from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main_app.models.department_model import department


# list department

def DepartmentList(request): 
    department_list = department.objects.all()
    
    return render(request, "main_app/department/department_list.html")