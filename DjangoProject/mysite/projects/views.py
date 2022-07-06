from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import Employee, Configuration
from django.template import loader
import json


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the project index.")


def details(request, fname): 
    employees = Employee.objects.filter(first_name__iexact = fname)

    template = loader.get_template('projects/detail.html')
    context = {
        'employees': employees,
        'fname': fname,
    }
    return HttpResponse(template.render(context, request))


def add_json_to_db(uploaded_file):

    uploaded_json_file = json.loads(uploaded_file.read())
    
    for data in uploaded_json_file:
        if "name" in data:
            if "content" in data:
                for content in data["content"]:
                    if "is_parent" in content and content["is_parent"] == "True":
                        if "field" in content and "xPath" in content:
                            field = content["field"].lower()
                            xpath = content["xPath"]
                            scheme_name = data["name"].lower()

                            if "parent_field" in content:
                                parent_field = content["parent_field"]
                            else:
                                parent_field = None
                            duplicate_data = Configuration.objects.filter(scheme_name = scheme_name, parent_field = parent_field, field = field).count()
                            
                            if duplicate_data == 0:
                                print("Create")
                                config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = True, field = field, xpath = xpath)
                                config.save()
                            
                            else:
                                print("Update")
                                config = Configuration.objects.get(scheme_name = scheme_name, parent_field = parent_field, field = field)
                                config.is_parent = True
                                config.xpath = xpath
                                config.save()

                        else:
                            print("Apple 33333333")

                            return False
 
                    if "is_parent" in content and (content["is_parent"] != "True" and content["is_parent"] != "False"):
                        return False
                    
            else:
                print("Apple 222222222")

                return False

        else:
            print("Apple 111111111111")
            return False

    for data in uploaded_json_file:
        if "name" in data:
            if "content" in data:
                for content in data["content"]:
                    if not ("is_parent" in content) or content["is_parent"] == "False":
                        if "field" in content and "xPath" in content:
                            field = content["field"].lower()
                            xpath = content["xPath"]
                            scheme_name = data["name"].lower()
                            if "parent_field" in content:
                                parent_field = content["parent_field"]
                            else:
                                parent_field = None

                            parent_exists = Configuration.objects.filter(scheme_name = scheme_name, field = parent_field, is_parent = True).count()

                            if parent_exists == 0:
                                print("Apple 777777777")
                                return False

                            else:
                                duplicate_data = Configuration.objects.filter(scheme_name = scheme_name, parent_field = parent_field, field = field).count()
                                
                                if duplicate_data == 0:
                                    print("Create")
                                    config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = False, field = field, xpath = xpath)
                                    config.save()
                                
                                else:
                                    print("Update")
                                    config = Configuration.objects.get(scheme_name = scheme_name, parent_field = parent_field, field = field)
                                    config.is_parent = False
                                    config.xpath = xpath
                                    config.save()

                        else:
                            print("Apple 777777777")
                            return False
 
                    if "is_parent" in content and (content["is_parent"] != "True" and content["is_parent"] != "False"):
                        print("Apple 66666666")
                        return False

            else:
                print("Apple 55555555")
                return False

        else:
            print("Apple 4444444444")

            return False
    
    return True
                

def upload(request): 
    context = {}
    if request.method == 'POST':
        if 'jsonfile' in request.FILES:
            uploaded_file = request.FILES['jsonfile']
            print(uploaded_file.name)

            if uploaded_file.content_type == 'application/json':
                flag = add_json_to_db(uploaded_file)
                if flag:
                    context['message'] = "Your file has been uploaded"
                else:
                    context['message'] = "The format of config file is not correct"
                
            
            else:
                context['message'] = "Please upload json file"

        else:
            context['message'] = "Please upload json file"

            

    return render(request, 'projects/upload.html', context)


def list_config(request):
    context = {}
    scheme_list = Configuration.objects.values_list('scheme_name', flat=True).distinct().order_by('scheme_name')
    context['scheme_list'] = scheme_list
    return render(request, 'projects/list_config.html', context)


def view_config(request, scheme_name):
    context = {}
    scheme_contents = Configuration.objects.filter(scheme_name=scheme_name)
    scheme_parent_content = Configuration.objects.filter(scheme_name=scheme_name, is_parent=True)
    context['scheme_contents'] = scheme_contents
    context['scheme_parent_content'] = scheme_parent_content
    context['scheme_name'] = scheme_name
    return render(request, 'projects/view_config.html', context)

    
