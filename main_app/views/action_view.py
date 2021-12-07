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
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from ..models.action_model import Action, auth_user_action
from main_app.forms.forms import ActionForm
from main_app.models.process_model import process_action
from django.contrib import messages
from django.db.models import ProtectedError

# Create your views here.


def IndexView(request):
    return redirect('/dashboard/')


action_success_url = "/dashboard/action/"


@login_required()
def ActionList(request):
    if request.user.has_perm('main_app.view_action'):
        data = []
        actions = Action.objects.all()
        for action in actions:
            users = auth_user_action.objects.filter(action_id=action)
            print(action,users)
            data.append((action,users))
        print(data)
        return render(request, "main_app/action_list.html", {"object_list":data, "title":"لیست وظایف"})
    else:
        return redirect('index') 

@login_required()
def ActionUpdate(request, pk):
    if request.user.has_perm('main_app.edit_action'):
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
            return render(request, "main_app/action_form_update.html", {"form": form, "obj":action_instance, "title":"بروزرسانی وظایف"})
        
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
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{action_instance.name} به روزرسانی شد.",
                    extra_tags="success",
                )                
                return redirect('action-list')
    else:
        return redirect('index')    
    
@method_decorator(login_required, name="dispatch")
class ActionDelete(DeleteView):
    model = Action
    title = "حذف وظیفه"
    def dispatch(self, *args, **kwargs):
        if not (
            self.request.user.is_superuser or
            self.request.user.has_perm('main_app.delete_action') 
        ):
            return redirect('index')
        return super(ActionDelete, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError as e:
            messages.add_message(
                    request,
                    messages.ERROR,
                    f"وظیفه {self.object.name} دارای وظیفه وابسته است و یا روندی از این وظیفه استفاده می‌کند و امکان حذف آن وجود ندارد.",
                    extra_tags="Danger",
                )
            messages.add_message(
                    request,
                    messages.WARNING,
                    f'برای حذف وظیفه "{self.object.name}"  ابتدا وظیفه وابسته یا روندهای مرتبط با این وظیفه را را پاکسازی کنید',
                    extra_tags="warning",
                )
            return redirect('action-list')
    
    template_name = "main_app/action_confirm_delete.html"
    success_url = action_success_url

@login_required()
def ActionCreate(request):
    if request.user.has_perm('main_app.create_action'):
        from main_app.models.action_model import auth_user_action
        if request.method == "GET":
            form = ActionForm()
            return render(request, "main_app/action_form.html", {"form": form,"title":"ساخت وظیفه جدید"})
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
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "وظیفه جدید ساخته شد",
                    extra_tags="success",
                )
                return redirect("action-list")
    else:
        return redirect('index')    