from django import forms
from crispy_forms.helper import FormHelper


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
