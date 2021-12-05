from django.db import models
from django.contrib.auth import get_user_model

class customer(models.Model):
    customer_name = models.CharField(max_length=55)
    customer_family = models.CharField(max_length=55)
    customer_mobile = models.CharField(max_length=11, unique=True)
    customer_phone = models.CharField(max_length=11, unique=True)
    operator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, editable=False)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return self.customer_name+" "+self.customer_family
    