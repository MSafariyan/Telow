from django.db import models
from django.contrib.auth import get_user_model
from main_app.models.process_model import process, process_action
from main_app.models.status_model import status
# Create your models here.

class order(models.Model):
    LASTMAN_STANDING = "DO OR DIE"
    CRITICAL_PRIORITY = "Critical"
    HIGH_PRIORITY = "High"
    MIDDLE_PRIORITY = "Middle"
    LOW_PRIORITY = "Low"

    INDEED_PRIORITY = [
        (LASTMAN_STANDING, 'Do or die'),
        (CRITICAL_PRIORITY, 'Critical priority'),
        (HIGH_PRIORITY, 'High priority'),
        (MIDDLE_PRIORITY, 'Middle priority'),
        (LOW_PRIORITY, 'Low priority'),
        
    ]
    
    order_title = models.CharField(max_length=100, unique=True)
    customer_id = models.ForeignKey(get_user_model(), null=True, on_delete=models.PROTECT)
    priority = models.CharField(max_length=11, choices=INDEED_PRIORITY, default=LOW_PRIORITY)
    process_id = models.ForeignKey(process, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return self.order_title

class order_meta(models.Model):
    order_id = models.OneToOneField(order, on_delete=models.CASCADE, primary_key=True)
    meta_value = models.JSONField(null=True)
    
    def __str__(self):
        return f" {self.order_id}"
    

class order_process_action(models.Model):
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    process_action = models.ForeignKey(process_action, on_delete=models.CASCADE)
    status = models.ForeignKey(status, on_delete=models.PROTECT, null=True,)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return f"___ action: {self.process_action}, ___ status: {self.status} |"