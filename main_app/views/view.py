from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from order.models import order, order_process_action
from main_app.models.process_model import process
from main_app.models.action_model import auth_user_action
from django.conf.urls import handler404

@login_required
def indexPanelView(request):
    order_count = order.objects.all().count()
    process_count = process.objects.all().count()
    active_process = process.objects.filter(isEnable=True).count()
    action_perms = auth_user_action.objects.filter(user_id__pk=request.user.pk).values_list('action_id', flat=True)
    related_order_id_to_current_user = order_process_action.objects.filter(process_action__action__in=action_perms).values_list('order_id').all()
    orders = order.objects.filter(pk__in=related_order_id_to_current_user).order_by('priority').all()
    return render(request, 'dashboard/dashboard.html', {"order_count":order_count, "process_count":process_count, "active_process":active_process,"orders":orders, "title":"پنل کاربری"})
    

def logout_view(request):
    logout(request)
    return redirect('index')
from django.core.exceptions import PermissionDenied

def handler404(request, exception):
    return render(request, 'main_app/404.html')

def handler500(request, exception):
    return render(request, 'main_app/500.html')