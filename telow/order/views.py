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

order_success_url = "/dashboard/order/"

@login_required()
def OrderCreat(request):
    if request.method == "GET":
        form = OrderForm()
        
        return render(request, "order/order_form.html", {"form":form})
    
    
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
    
            data = form.cleaned_data
            
            # hold model instance
            user_data = data['assignE']
            flow_data = data['flow']
            
            # serialize model instance that store them as a json object
            data['flow'] = serializers.serialize('json', [data['flow']])
            data['assignE'] = serializers.serialize('json', [data['assignE']])
            # data['flow'] = "چاپ کتاب"
            # data['assignE'] = "mahdi"
            print(data['assignE'])
            print(data['flow'])
            data['delivery_date'] = data['delivery_date'].strftime('%Y/%m/%d')
            
            # create order record on order table
            # creating meta needs to have a new instance of order
            # for some reasons title of each order must be uniqe
            try:
                new_order = order(order_title=data['title'], customer_id=user_data, priority=data['priority'], process_id=flow_data)
                new_order.save()
            except Exception as e:
                return JsonResponse({"Result":"BAD", "error":f'{e}'})
            # try to create order meta
            try:
                new_order_meta = order_meta(order_id=new_order, meta_value=data)
                new_order_meta.save()
            except Exception as e:
                return JsonResponse({"Result":"BAD", "error":f'{e}'})
            
            # try to create order actions
            try:
                actions = process_action.objects.filter(process_id=flow_data)
                status_action = status.objects.get(status_title="در دست بررسی")
                for action in actions:
                    new_order_meta = order_process_action(
                        order_id=new_order, process_action=action, status=status_action
                    )
                    new_order_meta.save()
            except Exception as e:
                return JsonResponse({"Result":"BAD", "error":f'{e}'})
            
            return JsonResponse({"Result":'OK','Fields':data}, safe=False)
            
        else:
            return HttpResponse(f"{form.errors.as_json()} ")

# @method_decorator(login_required, name="dispatch")
# class OrderCreat(CreateView):
#     model = order

#     fields = ["order_title", "customer_id", "priority", "process_id"]

#     def post(self, request):
#         order_title_form = self.request.POST.get("order_title")
#         customer_id_form = self.request.POST.get("customer_id")
#         priority_form = self.request.POST.get("priority")
#         process_form = self.request.POST.get("process_id")

#         assignE = User.objects.get(pk=customer_id_form)
#         process2 = process.objects.get(pk=int(process_form))

#         actions = process_action.objects.filter(process_id=process_form)

#         new_order = order(
#             order_title=order_title_form,
#             customer_id=assignE,
#             priority=priority_form,
#             process_id=process2,
#         )
#         new_order.save()

#         status_action = status.objects.get(status_title="در دست بررسی")
#         current_order = new_order

        # for action in actions:
        #     new_order_meta = order_meta(
        #         order_id=current_order, process_action=action, status=status_action
        #     )
        #     new_order_meta.save()

#         return redirect("order-list")

from order.models import order_meta
@login_required
def OrderDetail(request, pk):
    order_id = pk
    current_user = request.user
    current_order = order.objects.get(pk=pk)
    action_perms = auth_user_action.objects.filter(user_id=current_user).values_list('action_id', flat=True)
    actions2 = order_process_action.objects.filter(process_action__action__in=action_perms).filter(order_id=order_id).all()
    actions = order_process_action.objects.filter(order_id=current_order).all()
    meta = order_meta.objects.filter(order_id=order_id).only('meta_value').get()
    users = json.loads(meta.meta_value['assignE'])
    
    meta.meta_value['assignE'] = users
    # return HttpResponse(f"{meta.meta_value['title']} | {meta.meta_value['assignE']} | {meta.meta_value['flow']}")
    # print(users[0]['fields']['username'])
    return render(
        request, 
        "order/order_detail.html", 
        {"order": current_order, "actions": actions2, "meta":meta}
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
        print(order_meta_list)
    return render(request, "order/order_list.html", {"orders": order_meta_list})

# def OrderMetaStatus(request, pk):
#     order_meta_status = order_meta.objects.get(pk=pk)
    
#     return render(request, "order/order_meta_form.html", {"oder_meta":order_meta_status})
    
@method_decorator(login_required, name="dispatch")
class OrderMetaUpdate(UpdateView):
    template_name = 'order/order_meta_form.html'
    model = order_process_action
    fields = ['status']

    success_url = "/dashboard/order"
    
# def OrderMetaUpdate(request, pk):
#     obj = order_meta.objects.get(pk=pk)
#     form =
    
#     return HttpResponse(obj)