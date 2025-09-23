from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserLoginRegisterForm(forms.Form):
    phone = forms.CharField(max_length=11, required=True)


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone = (phone or '').strip()

        if not (phone.isdigit() and len(phone) == 11 and phone.startswith('09')):
            raise ValidationError('شماره موبایل معتبر نیست.')

        return phone

class OtpVerifyForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)



class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email", "bio", "age", "gender"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].required = False
        self.fields["age"].required = False
