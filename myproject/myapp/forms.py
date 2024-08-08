from django import forms

from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'gender', 'dob', 'phone']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match.")

        return cleaned_data
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'phone_no', 'license_no']
        # Note: `password`, `confirm_password`, and `license_number` are not fields in UserProfile


# myapp/forms.py
from django import forms
from .models import LabTechnician

class LabTechnicianForm(forms.ModelForm):
    class Meta:
        model = LabTechnician
        fields = ['specialization']
    # myapp/forms.py
