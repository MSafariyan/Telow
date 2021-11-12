from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Action(models.Model):
    name        = models.CharField(max_length=55, unique=True)
    description = models.CharField(max_length=155)
    dependency   = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    class Meta:
        ordering = ["pk"]
        
    def __str__(self):
        return self.name


class auth_user_action(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    action_id = models.ForeignKey(Action, on_delete=models.CASCADE)
    
    class Meta:
        pass
    
    def __str__(self):
        return f" {self.user_id} "