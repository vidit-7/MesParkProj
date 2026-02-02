from django import forms
from merchstore.models import Order

class OrderDeliveryForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('method_cod', 'Cash on Delivery'),
        ('method_stripe', 'Card (Stripe)'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = Order
        fields = ['phone','uemail','street','address','city','country','zipcode']
        labels = {
            'phone': 'Phone number',
            'uemail': 'Email address',
            'street': 'Block and Street',
            'address': 'Address',
            'city': 'City',
            'country': 'Country',
            'zipcode': 'Zip Code'
        }
        widgets = {
            'phone' : forms.TextInput(attrs={'class':'form-control','placeholder':'Your phone number...'}),
            'uemail' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Your email address...'}), #,'required':'true'
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
