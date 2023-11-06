# forms.py
from django import forms
from django.forms import TextInput,EmailInput
from .models import Loan, Payroll
from django.core.validators import MinValueValidator, MaxValueValidator

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email ','style': 'width: 50%;','class':'text-dark'}))
    subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Subject','style': 'width: 50%;','class':'text-dark'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Type messege here........','style': 'width: 50%;','class':'text-dark'}) )
    
    
class LoanForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Payroll.objects.all(),
        empty_label="Select an employee"
    )
    loan_amount = forms.DecimalField()
    loan_issue_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    loan_expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    payment_method = forms.ChoiceField(
        choices=[('percentage', 'Percentage Wise'), ('amount', 'Amount Wise')],
        initial='percentage'
    )

    # Define these fields based on the selected payment method
    monthly_cutting_percentage = forms.DecimalField(
        label="Monthly Cutting Percentage (%)",
        required=False,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    monthly_cutting_amount = forms.DecimalField(
        label="Monthly Cutting Amount (INR)",
        required=False,
    )

    class Meta:
        model = Loan
        fields = '__all__'
        
class EditLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['date_issue', 'date_expiry', 'loan_amount', 'monthly_cutting_type', 'monthly_cutting_percentage', 'monthly_cutting_amount']