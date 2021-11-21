from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from main_app.models.customer_model import customer
from django.contrib import messages
from main_app.forms.forms import CustomerForm
# Create your views here.

@login_required()
def CustomerList(request):
    if request.user.has_perm('main_app.view_customer'):
        customers = customer.objects.all()

        return render(request, "main_app/customer_list.html", {"coustomer_list":customers})
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "شما دسترسی لازم به این صفحه را ندارید",
            extra_tags="warning",
        )
        return redirect('index')
    
@login_required()
def CustomerCreate(request):
    if request.user.has_perm('create_customer'):
        if request.method == "GET":
            form = CustomerForm()
            return render(request, "main_app/customer_form.html", {"form":form})
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                new_customer = customer(customer_name=form.cleaned_data['customer_name'], customer_family=form.cleaned_data['customer_family'], customer_mobile=form.cleaned_data['customer_mobile'], customer_phone=form.cleaned_data['customer_phone'])
                new_customer.save()
                
                messages.add_message(request, messages.SUCCESS, "مشتری جدید با موفقیت ایجاد شد :)", extra_tags='success')
                return redirect('customer-list')
            else:
                return HttpResponse("Form is not valid")
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "شما دسترسی لازم به این صفحه را ندارید",
            extra_tags="warning",
        )
        return redirect('index') 
    
@login_required()
def CustomerUpdate(request, pk):
    if request.user.has_perm('update_customer'):
        current_customer = customer.objects.get(pk=pk)
        if request.method == "GET":
            data = {
                "customer_name":current_customer.customer_name,
                "customer_family":current_customer.customer_family,
                "customer_mobile":current_customer.customer_mobile,
                "customer_phone":current_customer.customer_phone
            }
            form = CustomerForm(initial=data)
            return render(request, "main_app/customer_form_update.html", {"form":form, "obj":current_customer})
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                current_customer.customer_name = form.cleaned_data['customer_name']
                current_customer.customer_family = form.cleaned_data['customer_family']
                current_customer.customer_mobile = form.cleaned_data['customer_mobile']
                current_customer.customer_phone = form.cleaned_data['customer_phone']
                current_customer.save()     
                messages.add_message(request, messages.SUCCESS, f" تغییرات در مشتری با نام {current_customer.customer_name} {current_customer.customer_family} با موفقیت اعمال شد.", extra_tags='success')
                return redirect('customer-list')
            else:
                return HttpResponse("Form is not valid")
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "شما دسترسی لازم به این صفحه را ندارید",
            extra_tags="warning",
        )
        return redirect('index') 