from django import forms
from suppticket.models import SupportTicket
from parktour.models import Booking
from merchstore.models import Order

class SupportTicketForm(forms.ModelForm):

    support_type = forms.ChoiceField(
        choices=[
            ("","--Select what you need support for--"),
            ("booking", "Booking"),
            ("order", "Order"),
            ("other", "Other")
        ],
        label="Support needed for",
        required=True
    )

    class Meta:
        model = SupportTicket
        fields = ["subject", "booking_sup", "ord_sup"]
        labels = {
            'subject': 'Describe the subject of your issue',
            'booking_sup': 'Choose the booking you need help with',
            'ord_sup': 'Choose the order you need help with',
        }
        widgets = {
            'subject' : forms.TextInput(attrs={'class':'form-control','placeholder':'Please describe your issue/query'}),
            # 'booking_sup' : forms.Select(attrs={'class':'form-control'}),
            # 'ord_sup' : forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        quser = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["booking_sup"].queryset = Booking.objects.filter(user=quser).order_by("-booked_at_date","-booking_date")
        self.fields["ord_sup"].queryset = Order.objects.filter(user=quser).order_by("-created_at")

    def clean(self):
        cleaned_data = super().clean()

        sup_type = cleaned_data.get("support_type")
        selected_booking = cleaned_data.get("booking_sup")
        selected_order = cleaned_data.get("ord_sup")

        if not sup_type:
            raise forms.ValidationError("Please select the type.")
        if selected_booking and selected_order:
            raise forms.ValidationError("Please select only one type.")
        if sup_type == "booking" and not selected_booking:
            raise forms.ValidationError("Please select the booking you need help with.")
        if sup_type == "order" and not selected_order:
            raise forms.ValidationError("Please select the order you need help with.")
        if sup_type == "other" and (selected_booking or selected_order):
            raise forms.ValidationError("Type \'Other\' can not accept booking or order")

        if selected_booking:
            cleaned_data["ord_sup"] = None
        elif selected_order:
            cleaned_data["booking_sup"] = None

        return cleaned_data