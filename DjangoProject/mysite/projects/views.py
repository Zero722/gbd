from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee
from django.template import loader


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the project index.")

def details(request, fname): 
    print(fname)
    employees = Employee.objects.filter(first_name__iexact = fname)

    template = loader.get_template('projects/detail.html')
    context = {
        'employees': employees,
        'fname': fname,
    }
    return HttpResponse(template.render(context, request))




    