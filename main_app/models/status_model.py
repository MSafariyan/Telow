from django.db import models

class status(models.Model):
    status_title = models.CharField(max_length=55, default='تعیین نشده')
    description = models.CharField(max_length=55, null=True)
    color = models.CharField(max_length=7, null=True, default='e3e3e3')
    editable = models.BooleanField(null=False,default=True)
    created_at   = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at   = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    class Meta:
        ordering = ["pk"]
        
    def __str__(self):
        return self.status_title
    