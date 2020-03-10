from django import forms
from django.forms import ModelForm
from inventory.models import PurchaseOrder, PurchaseItem

# class UserForm(UserCreationForm,ModelForm):
#     username = forms.CharField(min_length=3, max_length=30)
#     email = forms.EmailField(required = True)
#     first_name = forms.CharField(required =  True)
#     last_name = forms.CharField(required =True)

#     class Meta(UserCreationForm):
#         model = CustomUserBase
#         fields = ['first_name','last_name','email','username','user_type']


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(max_length = 32, widget= forms.PasswordInput)

#     class Meta: 
#         fields = ['username','password']

class PurchaseOrderForm(ModelForm):
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        exclude = ['added_by']


class PurchaseItemForm(ModelForm):
    
    class Meta:
        model = PurchaseItem
        fields = '__all__'
        exclude = ['added_by', 'purchase_order']