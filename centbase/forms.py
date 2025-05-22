from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from centbase.models import Profile

class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField( 
        max_length=28,
        required=True,
        widget= forms.TextInput(attrs={'class':'form-control','placeholder':'John'})
        )
    last_name = forms.CharField(
        max_length=28,
        required=True,
        widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Doe'})
        )

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2']
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control','placeholder':'johndoe1111'}),
        }

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField( 
        max_length=28,
        required=True,
        widget= forms.TextInput(attrs={'class':'form-control','placeholder':'John'})
        )
    last_name = forms.CharField(
        max_length=28,
        required=True,
        widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Doe'})
        )
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Your email...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about','pic','phone','street','address','city','country','zipcode']
        labels = {
            'about': 'About you',
            'pic': 'Profile picture',
            'phone': 'Phone number',
            'street': 'Block and Street',
            'address': 'Address',
            'city': 'City',
            'country': 'Country',
            'zipcode': 'Zip Code'
        }
        widgets = {
            'about' : forms.Textarea(attrs={'class':'form-control','placeholder':'About you...'}),
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

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        # print(self.fields.items())
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            # field.widget.attrs.update({'class': 'form-control'})

