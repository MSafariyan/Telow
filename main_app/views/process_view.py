from django.contrib.auth import models
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
from main_app.models.process_model import process, process_action
from main_app.models.status_model import status
from main_app.forms.forms import ProcessActionForm
from django.db import IntegrityError
from django.db.models import ProtectedError
from order.models import order, order_process_action
from django.contrib import messages


process_success_url = "/dashboard/process/"

@method_decorator(login_required, name="dispatch")
class ProcessList(ListView):
    model = process
    title = "لیست کاربران"
    def dispatch(self, *args, **kwargs):
        if not (
            self.request.user.is_superuser or
            self.request.user.has_perm('main_app.view_process') 
        ):
            return redirect('index')
        return super(ProcessList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
    
@login_required()
def ProcessDetail(request, pk):
    if request.user.has_perm('main_app.view_proccess'):
        current_process = process.objects.get(pk=pk)
        related_process_actions = process_action.objects.filter(process_id=current_process).all()
        return render(request, "main_app/process_detail.html", {"process":current_process, "process_action":related_process_actions, "title":"جزئیات روند"})
    else:
        return redirect('index')


@login_required()
def ProcessUpdate(request, pk):
    if request.user.has_perm('main_app.edit_process'):
        if request.method == "GET":
            current_process = process.objects.get(pk=pk)
            all_process_action = process_action.objects.filter(
                process_id=current_process
            ).all()
            data = {
                "name": current_process.process_name,
                "description": current_process.process_description,
                "isEnable": current_process.isEnable,
                "actions": all_process_action.values_list("action", flat=True),
            }
            form = ProcessActionForm(initial=data)
            return render(
                request,
                "main_app/process_form_update.html",
                {"form": form, "obj": current_process, "title":"به روزرسانی روند"},
            )

        if request.method == "POST":
            process_instance = process.objects.get(pk=pk)
            form = ProcessActionForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                description = form.cleaned_data.get("description")
                actions = form.cleaned_data.get("actions")
                status_form = form.cleaned_data.get("isEnable")
                process_instance.process_name = name
                process_instance.process_description = description
                process_instance.isEnable = status_form
                process_instance.save()
                # delete unrelated process_actions
                must_delete_actions = []
                all_process_action = process_action.objects.filter(
                    process_id=process_instance
                ).all()
                for PA in all_process_action:
                    if PA.action not in actions:
                        process_action.objects.filter(action=PA.action).delete()

                for action in actions:
                    (
                        new_process_action,
                        new_process_action_status,
                    ) = process_action.objects.update_or_create(
                        process_id=process_instance, action=action
                    )
                    new_process_action.save()
                all_process_action = process_action.objects.filter(
                    process_id=process_instance
                ).all()
                # all related actions to current process
                actions = process_action.objects.filter(process_id=process_instance).all()
                # get all orders related to current process
                all_order_realted_to_current_process = order.objects.filter(process_id=process_instance).all()
                status_action = status.objects.get(status_title="در دست بررسی")
                # updated each order meta
                for each_order in all_order_realted_to_current_process:
                    all_order_meta_for_each_order = order_process_action.objects.filter(order_id=each_order).all()
                    for action in actions:
                        order_process_action.objects.update_or_create(
                            process_action=action, order_id=each_order
                        )
                data = {
                    "name": process_instance.process_name,
                    "description": process_instance.process_description,
                    "isEnable": process_instance.isEnable,
                    "actions": all_process_action.values_list("action", flat=True),
                }
                form = ProcessActionForm(initial=data)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{process_instance.process_name} به روز شد.",
                    extra_tags="success",
                )
                return redirect('process-list')
                # update related orders
                # return render(
                #     request,
                #     "main_app/process_form_update.html",
                #     {
                #         "form": form,
                #         "message": message,
                #         "status": "success",
                #         "obj": process_instance,
                #     },
                # )
    else:
        return redirect('index')


@method_decorator(login_required, name="dispatch")
class ProcessDelete(DeleteView):
    model = process
    success_url = process_success_url
    title = "حذف روند"
    def dispatch(self, *args, **kwargs):
        if not (
            self.request.user.is_superuser or
            self.request.user.has_perm('main_app.delete_process') 
        ):
            return redirect('index')
        return super(ProcessDelete, self).dispatch(*args, **kwargs)

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
                    f"روند {self.object.process_name} دارای وظایف مرتبط است و امکان حذف آن وجود ندارد.",
                    extra_tags="Danger",
                )
            messages.add_message(
                    request,
                    messages.WARNING,
                    f'برای حذف روند "{self.object.process_name}"  ابتدا وظایف مرتبط را پاکسازی کنید',
                    extra_tags="warning",
                )
            return redirect('process-list')

    success_url = process_success_url


@login_required()
def ProcessCreate(request):
    if request.user.has_perm('main_app.create_process'):
        if request.method == "GET":
            form = ProcessActionForm
            return render(request, "main_app/process_form.html", {"form": form, "title":"ساخت روند جدید"})
        if request.method == "POST":
            form = ProcessActionForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                description = form.cleaned_data.get("description")
                actions = form.cleaned_data.get("actions")
                status = form.cleaned_data.get("isEnable")
                new_process = process(
                    process_name=name, process_description=description, isEnable=status
                )
                try:
                    new_process.save()
                except IntegrityError as e:
                    data = {
                        "name": name,
                        "description": description,
                        "actions": actions,
                        "isEnable": form.cleaned_data.get("isEnable"),
                    }
                    form = ProcessActionForm(initial=data)
                    message = (
                        f"روندی با نام {name} از قبل وجود دارد. لطفا نام دیگری انتخاب کنید"
                    )
                    return render(
                        request,
                        "main_app/process_form.html",
                        {"form": form, "message": message, "status": "danger"},
                    )
                for action in actions:
                    new_process_action = process_action(
                        process_id=new_process, action=action
                    )
                    new_process_action.save()
                form = ProcessActionForm
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "روند جدید ساخته شد",
                    extra_tags="success",
                )
                return redirect('process-list')
            else:
                return HttpResponse(form.errors)
    else:
        return redirect('index')