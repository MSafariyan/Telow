from django.contrib import admin
from main_app.models.action_model import Action, auth_user_action
from .models.status_model import status
from .models.process_model import process, process_action
from order.models import order, order_process_action, order_meta
from main_app.models.department_model import department
from main_app.models.customer_model import customer

# Register your models here.

# class ordermetaAdmin(admin.ModelAdmin):
#     list_display = ['pk','order_id', 'process_action', 'status', 'updated_at']

# class process_actionAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'process_id', 'action', 'updated_at']
  
class authUserActionAdmin(admin.ModelAdmin):
      list_display = ['pk', 'user_id', 'action_id']  
    
class orderProcessActionAdmin(admin.ModelAdmin):
      list_display = ['pk', 'order_id', 'process_action', 'status']

class orderMetaAdmin(admin.ModelAdmin):
      list_display = ['pk', 'order_id', 'meta_value']
      
admin.site.register(Action)
admin.site.register(auth_user_action, authUserActionAdmin)
admin.site.register(status)
admin.site.register(order)
admin.site.register(order_process_action, orderProcessActionAdmin)
admin.site.register(process)
admin.site.register(process_action)
admin.site.register(department)
admin.site.register(order_meta, orderMetaAdmin)
admin.site.register(customer)