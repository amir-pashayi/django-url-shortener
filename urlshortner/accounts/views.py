from django.shortcuts import render,redirect
from django.views import View
from .forms import UserLoginRegisterForm
from .models import OTP, User
from django.utils import timezone
from .services import send_otp_code
from django.conf import settings


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

            cooldown = getattr(settings, "OTP_RESEND_COOLDOWN", 120)
            otp = OTP.objects.filter(phone=phone).first()
            if otp:
                elapsed = (timezone.now() - otp.created_at).total_seconds()
                if elapsed < cooldown:
                    form.add_error('phone', f'Please wait {int(cooldown - elapsed)} seconds before trying again')
                    return render(request, self.template_name, {'form': form})
                otp.delete()

            otp = OTP.objects.create(phone=phone, code=OTP.generate_otp(), created_at=timezone.now())
            send_otp_code(phone, otp.code)
            return redirect('home')
        return render(request, self.template_name, {'form': form})