from django import forms
from django.core.exceptions import ValidationError


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


class UserRegisterForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    username = forms.CharField(max_length=100, required=True)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    bio = forms.CharField(widget=forms.Textarea, required=False)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
