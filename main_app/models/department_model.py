from django.db import models

class department(models.Model):
    depart_name = models.CharField(max_length=55)
    depart_description = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.depart_name