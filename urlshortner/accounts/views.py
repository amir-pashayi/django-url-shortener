from django.shortcuts import render,redirect
from django.views import View
from .forms import UserLoginRegisterForm
from .models import OTP
from django.utils import timezone
from .services import send_otp_code


class LoginView(View):
    form_class = UserLoginRegisterForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            otp = OTP.objects.create(phone=phone, code=OTP.generate_otp(), created_at=timezone.now())
            # send_otp_code(phone, otp)
            return redirect('home')
        return render(request, self.template_name, {'form': form})