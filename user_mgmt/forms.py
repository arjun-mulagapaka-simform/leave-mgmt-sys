from user_mgmt.models import Employee
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Employee
from crispy_forms.helper import FormHelper

class EmployeeCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ("email", "first_name", "last_name", "department", "role")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # important
        if commit:
            user.save()
        return user


class EmployeeChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Employee
        fields = "__all__"

    def clean_password(self):
        return self.initial["password"]


class EmployeeLoginForm(forms.Form):
    """
    Login form for Employee
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
