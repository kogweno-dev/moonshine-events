from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name", "phone", "email", "event_type", "event_date", "guests",
                  "budget", "venue", "catering_package", "message"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "guests": forms.NumberInput(attrs={"min": 1, "placeholder": "e.g. 200"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Theme, colours, menu ideas, anything we should know"}),
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "placeholder": "07xx xxx xxx"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }
        labels = {
            "name": "Full name",
            "phone": "Phone / WhatsApp",
            "email": "Email address",
            "event_type": "Type of event",
            "event_date": "Preferred date",
            "guests": "Expected guests",
            "budget": "Budget range (KSh)",
            "venue": "Venue or town",
            "catering_package": "Catering package",
            "message": "Tell us about your event",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["catering_package"].required = False
        self.fields["catering_package"].empty_label = "No catering / not sure yet"


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
