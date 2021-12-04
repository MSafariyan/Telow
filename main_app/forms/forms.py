from django import forms
from main_app.models.action_model import Action
from main_app.models.status_model import status
from main_app.models.process_model import process
from order.models import order_process_action
from django.contrib.auth import get_user_model

class ActionForm(forms.Form):
    """ 
        Create or edit actions
        
        Keywords:
        name        -- the name of action
        description -- the description of action
    """
    class Meta:
        model = Action

    name = forms.CharField(
        label="نام عملیات",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام عملیات"}
        ),
    )
    description = forms.CharField(
        label="توضیحات",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "توضیحات"}
        ),
    )


class StatusForm(forms.Form):
    """
        Status of actions in Process_action table,
        
        Keywords:
        name        -- the name of status
        description -- the description of status
        color       -- the color of status button in view
    """
    class Meta:
        model = status

    name = forms.CharField(
        label="نام وضعیت",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        required=False,
        label="توضیحات",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    color = forms.CharField(
        required=False,
        label="رنگ وضعیت",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class OrderMetaForm(forms.Form):
    """
        Change status of process_actions
    """
    status = forms.ModelMultipleChoiceField(
        queryset=status.objects.all(), label="وضعیت"
    )

    class Meta:
        model = order_process_action


class ActionForm(forms.Form):
    
    name = forms.CharField(
        label="نام وظیفه", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="توضیحات", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    dependency = forms.ModelChoiceField(
        queryset=Action.objects.all(),
        required=False,
        label="وظیفه وابسته",
        widget=forms.Select(attrs={"class": "js-example-basic-single form-control"}),
    )
    assignE = forms.ModelMultipleChoiceField(
        required=False,
        queryset= get_user_model().objects.filter(is_staff=True).all(),
        label="کاربران دارای دسترسی به این وظیفه",
        widget=forms.SelectMultiple(attrs={"class":"js-example-basic-single form-control"}),
    )
    


class ProcessActionForm(forms.Form):
    name = forms.CharField(
        required=True,
        label="نام روند",
        widget=forms.TextInput(attrs={"class":"form-control"}),
    )
    description = forms.CharField(
        label="توضیحات",
        widget=forms.TextInput(attrs={"class":"form-control",})
    )
    actions = forms.ModelMultipleChoiceField(
        queryset=Action.objects.all(),
        required=False,
        label="وظایف مرتبط",
        widget=forms.SelectMultiple(attrs={"class":"js-example-basic-single form-control"}),
    )
    isEnable = forms.BooleanField(
        required=False,
        label="روند فعال شود؟",
        widget=forms.CheckboxInput(attrs={'class':''})
    )
    
    
class CustomerForm(forms.Form):
    customer_name = forms.CharField(
        required=True,
        label="نام مشتری",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    
    customer_family = forms.CharField(
        required=True,
        label="نام خانوادگی مشتری",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    
    customer_mobile = forms.CharField(
        required=True,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={'class':'form-control', 'maxlength':'11'})
    )
    
    customer_phone = forms.CharField(
        required=True,
        label="شماره تماس ثابت",
        widget=forms.TextInput(attrs={'class':'form-control', 'maxlength':'11'})
    )