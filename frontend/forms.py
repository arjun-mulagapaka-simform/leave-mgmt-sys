from django import forms
from crispy_forms.helper import FormHelper
from leavemanagement.models import LeaveLog
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


class LeaveRequestForm(forms.ModelForm):
    """
    Leave request form for Employee
    """

    class Meta:
        model = LeaveLog
        fields = ("leave_type", "start_date", "end_date", "reason")
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tage = False
        