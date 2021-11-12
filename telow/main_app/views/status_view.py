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

@login_required()
def StatusCreate(request):
    if request.method == "GET":
        form = StatusForm()
        
        return render(request, "main_app/status_form.html", {"form":form})
    
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            new_status = status(status_title=form.cleaned_data['name'], description=form.cleaned_data['description'], color=form.cleaned_data['color'])
            new_status.save()
            
            return redirect('status-list')
            
@login_required()
def StatusUpdate(request, pk):
    if request.method == "GET":
        current_status = status.objects.get(pk=pk)
        data = {
            "name": current_status.status_title,
            "description": current_status.description,
            "color": current_status.color
        }
        form = StatusForm(initial=data)
        return render(request, "main_app/status_form_update.html", {"form":form, "obj":current_status})
    
    if request.method == "POST":
        form = StatusForm(request.POST)
        current_status = status.objects.get(pk=pk)
        if form.is_valid():
            current_status.status_title = form.cleaned_data['name']
            current_status.description = form.cleaned_data['description']
            current_status.color = form.cleaned_data['color']
            current_status.save()
            
            return redirect("status-list")
            
            

        


@method_decorator(login_required, name="dispatch")
class StatusDelete(DeleteView):
    model = status

    success_url = status_success_url
