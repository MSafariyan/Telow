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
from django.http import HttpResponse
from django.views import View
from ..models.status_model import status
from main_app.forms.forms import StatusForm
from django.contrib.auth.decorators import login_required

status_success_url = "/dashboard/status/"

@method_decorator(login_required, name="dispatch")
class StatusList(ListView):
    model = status
    title = "لیست وضعیت‌ها"
    def dispatch(self, *args, **kwargs):
        if not (
            self.request.user.is_superuser or
            self.request.user.has_perm('main_app.view_status') 
        ):
            return redirect('index')
        return super(StatusList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

@login_required()
def StatusCreate(request):
    if request.user.has_perm('main_app.create_status'):
        if request.method == "GET":
            form = StatusForm()
            
            return render(request, "main_app/status_form.html", {"form":form, "title":"ساخت وضعیت جدید"})
        
        if request.method == "POST":
            form = StatusForm(request.POST)
            if form.is_valid():
                new_status = status(status_title=form.cleaned_data['name'], description=form.cleaned_data['description'], color=form.cleaned_data['color'])
                new_status.save()
                
                return redirect('status-list')
    else:
        return redirect('index')      
            
@login_required()
def StatusUpdate(request, pk):
    if request.user.has_perm('main_app.edit_status'):
        if request.method == "GET":
            current_status = status.objects.get(pk=pk)
            data = {
                "name": current_status.status_title,
                "description": current_status.description,
                "color": current_status.color
            }
            form = StatusForm(initial=data)
            return render(request, "main_app/status_form_update.html", {"form":form, "obj":current_status, "title":"بروزرسانی وضعیت"})
        
        if request.method == "POST":
            form = StatusForm(request.POST)
            current_status = status.objects.get(pk=pk)
            if form.is_valid():
                current_status.status_title = form.cleaned_data['name']
                current_status.description = form.cleaned_data['description']
                current_status.color = form.cleaned_data['color']
                current_status.save()
                
                return redirect("status-list")
    else:
        return redirect('index')            
            

        


@method_decorator(login_required, name="dispatch")
class StatusDelete(DeleteView):
    model = status
    title = "حذف وضعیت"
    def dispatch(self, *args, **kwargs):
        if not (
            self.request.user.is_superuser or
            self.request.user.has_perm('main_app.delete_status') 
        ):
            return redirect('index')
        return super(StatusDelete, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    success_url = status_success_url
