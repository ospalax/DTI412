from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'student_id', 'faculty')

from .models import InternshipRequest

class InternshipRequestForm(forms.ModelForm):
    class Meta:
        model = InternshipRequest
        fields = ['company_name', 'position']
