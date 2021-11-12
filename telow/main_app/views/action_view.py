from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from ..models.action_model import Action, auth_user_action
from main_app.forms.forms import ActionForm
from main_app.models.process_model import process_action

# Create your views here.


def IndexView(request):
    return redirect('/dashboard/')


action_success_url = "/dashboard/action/"


@login_required()
def ActionList(request):
    data = []
    actions = Action.objects.all()
    for action in actions:
        users = auth_user_action.objects.filter(action_id=action)
        print(action,users)
        data.append((action,users))
    print(data)
    return render(request, "main_app/action_list.html", {"object_list":data})

# @method_decorator(login_required, name="dispatch")
# class ActionList(ListView):
#     template_name = "main_app/action_list.html"
#     queryset = Action.objects.all()
    

@login_required()
def ActionUpdate(request, pk):
    from main_app.models.action_model import auth_user_action
    if request.method == "GET":
        action_instance = Action.objects.get(pk=pk)
        users = auth_user_action.objects.filter(action_id=action_instance)
        data = {
            "name": action_instance.name,
            "description": action_instance.description,
            "dependency": action_instance.dependency,
            "assignE": users.values_list('user_id', flat=True)
        }
        form = ActionForm(initial=data)
        return render(request, "main_app/action_form_update.html", {"form": form, "obj":action_instance})
    
    if request.method == "POST":
        action_instance = Action.objects.get(pk=pk)
        form = ActionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            dependency = form.cleaned_data.get('dependency')
            users = form.cleaned_data.get('assignE')
            action_instance.name = name
            action_instance.description = description
            action_instance.dependency = dependency
            action_instance.save()
            # delete all realted user permisions to action
            auth_user_action.objects.filter(action_id=action_instance).delete()
            
            for user in users:
                new_auth_user_action = auth_user_action(user_id=user, action_id=action_instance)
                new_auth_user_action.save()
                
            # initial data to prepopulate form 
            users = auth_user_action.objects.filter(action_id=action_instance)

            data = {
                "name": action_instance.name,
                "description": action_instance.description,
                "dependency": action_instance.dependency,
                "assignE": users.values_list('user_id', flat=True)
            }
            form = ActionForm(initial=data)
            message = "وظیفه به روزرسانی شد"
            return render(request, "main_app/action_form_update.html", {"form":form,'message':message, "status":"success", "obj":action_instance})
        
              
@method_decorator(login_required, name="dispatch")
class ActionDelete(DeleteView):
    model = Action
    template_name = "main_app/action_confirm_delete.html"
    success_url = action_success_url

@login_required()
def ActionCreate(request):
    from main_app.models.action_model import auth_user_action
    if request.method == "GET":
        form = ActionForm()
        return render(request, "main_app/action_form.html", {"form": form})
    
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            description=form.cleaned_data.get('description')
            dependency=form.cleaned_data.get('dependency')
            users = form.cleaned_data.get('assignE')
            new_action = Action(name=name, description=description, dependency=dependency)
            try:
                new_action.save()
            except IntegrityError as e:
                data = {
                    "name":name,
                    "description":description,
                    "dependency":dependency,
                    "assignE":users,
                }
                form = ActionForm(initial=data)
                message = f"روند {name} از قبل وجود دارد. لطفا نام جدیدی انتخاب کنید."
                return render(request, "main_app/action_form.html", {"form":form, "message":message, "status":"danger"})
            for user in users:
                new_auth_user_action = auth_user_action(user_id=user, action_id=new_action)
                new_auth_user_action.save()
            form = ActionForm()
            message = "وظیفه جدید ساخته شد"
            return render(request, "main_app/action_form.html", {"form":form,'message':message, "status":"success"})
                
                
                
                
                
                
                
                
                
                
                
            return redirect('action-list')
        else:
            return HttpResponse("False")
        