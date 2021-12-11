from os import stat
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from order.models import order, order_process_action
from main_app.models.process_model import process, process_action
from main_app.models.action_model import auth_user_action
from main_app.models.status_model import status
from django.conf.urls import handler404
from django.core import serializers
from django.db.models import Q

@login_required
def indexPanelView(request):
    order_count = order.objects.all().count()
    process_count = process.objects.all().count()
    active_process = process.objects.filter(isEnable=True).count()
    action_perms = auth_user_action.objects.filter(user_id__pk=request.user.pk).values_list('action_id', flat=True)
    finished = status.objects.filter(status_title="پایان یافته").first()
    related_order_id_to_current_user = order_process_action.objects.filter(process_action__action__in=action_perms).filter(~Q(status=finished)).values_list('order_id').all()
    orders = order.objects.filter(pk__in=related_order_id_to_current_user).order_by('priority').all()
    
    under_check = status.objects.filter(status_title="در دست بررسی").first()
    current_user = request.user
    active_duties = order_process_action.objects.filter(~Q(status=finished)).filter(process_action__action__auth_user_action__user_id=current_user).values_list('order_id').all()
    active_order_duties = order.objects.filter(pk__in=active_duties)

    return render(request, 'dashboard/dashboard.html', {"title":"پنل کاربری", "order_count":order_count, "process_count":process_count, "active_process":active_process, "active_duties":active_order_duties, "orders":orders})
    

def logout_view(request):
    logout(request)
    return redirect('index')
from django.core.exceptions import PermissionDenied

def handler404(request, exception):
    return render(request, 'main_app/404.html')

def handler500(request, exception):
    return render(request, 'main_app/500.html')