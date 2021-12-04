from django.db import models
from .action_model import Action
from .status_model import status

class process(models.Model):
    process_name = models.CharField(max_length=155, unique=True)
    process_description = models.CharField(max_length=500)
    isEnable = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return self.process_name

class process_action(models.Model):
    action   = models.ForeignKey(Action, on_delete=models.PROTECT)
    process_id   = models.ForeignKey(process, on_delete=models.PROTECT, null=False, default="تعیین نشده")
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    
    def __str__(self):
        return self.action.name

    
    