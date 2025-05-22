from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from merchstore.models import Order

class OrderDeliveryForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone','street','address','city','country','zipcode']
        labels = {
            'phone': 'Phone number',
            'street': 'Block and Street',
            'address': 'Address',
            'city': 'City',
            'country': 'Country',
            'zipcode': 'Zip Code'
        }
        widgets = {
            'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'Your phone number...'}),
            'street' : forms.TextInput(attrs={'class':'form-control','placeholder':'Your block and street...'}),
            'address' : forms.Textarea(attrs={'class':'form-control','placeholder':'Your area\'s address...'}),
            'city' : forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),
            # 'country': forms.TextInput(attrs={'class':'form-control','placeholder':'Your country...'}),
            'country': forms.Select(choices=[('','Select your country'),
                                            ('Australia','Australia'),
                                            ('Brazil','Brazil'),
                                            ('Costa Rica', 'Costa Rica'),
                                            ('Dominican Republic', 'Dominican Republic'),
                                            ('France','France'),
                                            ('Germany','Germany'),
                                            ('India','India'),
                                            ('Indonesia','Indonesia'),
                                            ('Italy','Italy'),
                                            ('Malaysia','Malaysia'),
                                            ('New Zealand','New Zealand'),
                                            ('UK','UK'),
                                            ('USA','USA'),
                                            ],
                                            attrs={
                                                'class':'form-control',
                                                'title':'Choose your country'
                                            }
                                        ),
            'zipcode': forms.TextInput(attrs={'class':'form-control','placeholder':'zip-code'}),
        }
