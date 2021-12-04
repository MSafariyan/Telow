from django.db import models
from django.contrib.auth import get_user_model
from main_app.models.process_model import process, process_action
from main_app.models.status_model import status
from main_app.models.customer_model import customer


# Create your models here.

class order(models.Model):
    # This model just save main data of orders like title, customer's name, priority, and etc
    
    INDEED_PRIORITY = [
        ("DO OR DIE", 'Do or die'),
        ("Critical", 'Critical priority'),
        ("High", 'High priority'),
        ("Middle", 'Middle priority'),
        ( "Low", 'Low priority'),
        
    ]
    
    order_title = models.CharField(max_length=100, unique=True)
    customer_id = models.ForeignKey(customer, null=True, on_delete=models.PROTECT)
    priority = models.CharField(max_length=11, choices=INDEED_PRIORITY, default="Low priority")
    process_id = models.ForeignKey(process, on_delete=models.SET_NULL, null=True)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return self.order_title

class order_meta(models.Model):
    """
        other details of order in Fatty(OrderForm) form will save as a json with this model
    """
    
    order_id = models.OneToOneField(order, on_delete=models.CASCADE, primary_key=True)
    meta_value = models.JSONField(null=True)
    
    """
        because this app is just a local private service for our company,
        we need have some custome permission to show each section of order form
        to related department
    """
    class Meta:
        permissions = [
            ("Can_view_litography", "can view litography details"),
            ("Can_view_paper", "can view paper details"),
            ("Can_view_hotstamp", "can view hotstamp details"),
            ("Can_view_befor_cut", "can view befor cut details"),
            ("Can_view_print",  "can view print details"),
            ("Can_view_hard_cover", "can view hard cover details"),
            ("Can_view_plastic_cover", "can view plastice cover details"),
            ("Can_view_part_cover", "can view part cover details"),
            ("Can_view_shield", "can view sheidl details"),
            ("Can_view_window_sticking", "can view window sticking details"),
            ("Can_view_box_sticking", "can view box sticking details"),
            ("Can_view_bindray", "can view bindray details"),
            ("Can_view_customize", "can view customize details"),
            ("Can_view_packaging", "can view packaging details")
            
        ]
    
    def __str__(self):
        return f" {self.order_id}"
    

class order_process_action(models.Model):
    """
        process actions are the actions that you declear and connect it to a process then 
        each order form have their own process actions
    """
    order_id = models.ForeignKey(order, on_delete=models.CASCADE)
    process_action = models.ForeignKey(process_action, on_delete=models.CASCADE)
    status = models.ForeignKey(status, on_delete=models.PROTECT, null=True,)
    created_at  = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at  = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return f"___ action: {self.process_action}, ___ status: {self.status} |"