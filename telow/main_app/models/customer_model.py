from django.db import models

class customer(models.Model):
    customer_name = models.CharField(max_length=55)
    customer_family = models.CharField(max_length=55)
    customer_mobile = models.CharField(max_length=11, unique=True)
    customer_phone = models.CharField(max_length=11, unique=True)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return self.customer_name+" "+self.customer_family
    