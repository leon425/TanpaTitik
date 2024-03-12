from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm): #Replicate the original user creation form (UserCreationForm)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']


# SHIPPING ADDRESS
class LocationForm(forms.Form):    
    province = forms.ModelChoiceField(queryset=Province.objects.all(),
                                      widget=forms.Select(attrs={"hx-get":"/load_cities/","hx-post":"load_cities/", "hx-target":"#id_city","hx-trigger":"change", })
                                      )
    city = forms.ModelChoiceField(queryset=City.objects.none())
    district = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)
    zipcode = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "province" in self.data:
            province_id = int(self.data.get("province"))
            self.fields["city"].queryset = City.objects.filter(province_id=province_id)


# PAYMENT EVIDENCE
class PaymentEvidence(forms.Form):
    payment_evidence = forms.ImageField()

# ORDER.STATUS (SUPERUSERPAGE)
class SetOrderStatus(forms.Form):
    status = forms.ModelChoiceField(queryset=OrderStatus.objects.all())
#["Cancelled","Placed","Pending (Waiting For Verification)", "Packaged", "On Delivery", "Delivered"]