from django.shortcuts import render, redirect
from main_app.models.action_model import Action, auth_user_action
from main_app.models.process_model import process
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from main_app.models.process_model import *
from django.contrib.auth.models import User
from order.models import order, order_process_action
import json
from django.core import serializers
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from main_app.forms.forms import OrderMetaForm
from order.forms import OrderForm
from django.http import JsonResponse
import json
from django.core import serializers
from order.models import order_meta
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from order.models import order_meta
from django.contrib import messages
from order.models import order_meta

order_success_url = "/dashboard/order/"


@login_required()
def OrderCreat(request):
    if request.user.has_perm("order.create_order"):
        if request.method == "GET":
            form = OrderForm()
            return render(request, "order/order_form.html", {"form": form, "title":'ساخت سفارش جدید'})
        if request.method == "POST":
            form = OrderForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES

                data = form.cleaned_data

                for file in files.items():
                    fs = FileSystemStorage()
                    filename = fs.save(file[1].name, file[1])
                    print(filename)
                    uploaded_file_url = fs.url(filename)
                    print(uploaded_file_url)
                    data[file[0]] = {
                        "name": file[1].name,
                        "location": uploaded_file_url,
                    }

                # hold model instance
                user_data = data["assignE"]
                flow_data = data["flow"]
                
                # serialize model instance to have json format
                data["flow"] = serializers.serialize("json", [data["flow"]])
                data["assignE"] = serializers.serialize("json", [data["assignE"]])
                data["delivery_date"] = data["delivery_date"].strftime("%Y/%m/%d")
                
                # create order record on order table
                # creating meta needs to have a new instance of order
                # for some reasons title of each order must be uniqe
                try:
                    new_order = order(
                        order_title=data["title"],
                        customer_id=user_data,
                        priority=data["priority"],
                        process_id=flow_data,
                    )
                    new_order.save()
                except Exception as e:
                    return JsonResponse({"Result": "BAD, when creating new order", "error": f"{e}"})
                # try to create order meta
                try:
                    data["operator"] = {
                        "username":request.user.username
                    }
                    new_order_meta = order_meta(order_id=new_order, meta_value=data)
                    new_order_meta.save()
                except Exception as e:
                    return JsonResponse({"Result": "BAD", "error": f"{e}"})

                # try to create order actions
                try:
                    actions = process_action.objects.filter(process_id=flow_data)
                    status_action = status.objects.get(status_title="در دست بررسی")
                    for action in actions:
                        new_order_meta = order_process_action(
                            order_id=new_order,
                            process_action=action,
                            status=status_action,
                        )
                        new_order_meta.save()
                except Exception as e:
                    return JsonResponse({"Result": "BAD", "error": f"{e}"})

                return redirect("order-list")

            else:
                return HttpResponse(f"{form.errors.as_json()} ")
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "شما دسترسی لازم به این صفحه را ندارید",
            extra_tags="warning",
        )
        return redirect("order-list")


@login_required
def OrderDetail(request, pk):
    order_id = pk
    current_user = request.user
    current_order = order.objects.get(pk=pk)
    action_perms = auth_user_action.objects.filter(user_id=current_user).values_list(
        "action_id", flat=True
    )
    from main_app.models.status_model import status

    Status = status.objects.get(status_title="پایان یافته")
    actions2 = (
        order_process_action.objects.filter(process_action__action__in=action_perms)
        .filter(order_id=order_id)
        .all()
    )
    actions = order_process_action.objects.filter(order_id=current_order).order_by("id").all()
    meta = order_meta.objects.filter(order_id=order_id).only("meta_value").get()
    users = json.loads(meta.meta_value["assignE"])
    meta.meta_value["assignE"] = users

    return render(
        request,
        "order/order_detail.html",
        {
            "order": current_order,
            "actions": actions,
            "UserActions": actions2,
            "meta": meta,
            "finished": Status,
            "title":"جزئیات سفارش"
        },
    )


@login_required
def OrderListView(request):
    order_list = order.objects.all()
    order_meta_list = []
    serialized_queryset = serializers.serialize("json", order_list)

    for order_metas in order_list:
        meta = (
            order_process_action.objects.filter(order_id=order_metas)
            .order_by("-updated_at")
            .first()
        )
        order_meta_list.append({"order": order_metas, "order_meta": meta})
    return render(request, "order/order_list.html", {"orders": order_meta_list, "title":"لیست سفارشات"})


@method_decorator(login_required, name="dispatch")
class OrderMetaUpdate(UpdateView):
    template_name = "order/order_meta_form.html"
    model = order_process_action
    fields = ["status"]
    title = "بروزرسانی سفارش"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    success_url = "/dashboard/order"

from django.core import serializers
from django.contrib.postgres.search import SearchVector
import json
from jalali_date import datetime2jalali, date2jalali

@login_required
def order_search(request):
    if request.method == 'GET':
        if request.GET.get('q') is not None and request.GET.get('q') != u"":
            search_value = request.GET.get('q')
            query = order.objects.annotate(search=SearchVector('order_title', 'customer_id__customer_name', 'customer_id__customer_family')).filter(search=search_value).all()
            list_data = []
            for data in query:
                temp_list_data = {"order_id":data.pk, "order_title":data.order_title, "customer":data.customer_id.customer_name+" "+data.customer_id.customer_family, "priority":data.priority, "process":data.process_id.process_name, "created_at": datetime2jalali(data.created_at).strftime(' - %Y/%m/%d - %H:%M')}
                list_data.append(temp_list_data)
        else:
            result = {"result": "None"}

        return JsonResponse(list_data,safe=False)