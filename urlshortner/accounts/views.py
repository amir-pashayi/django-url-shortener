from django.shortcuts import render,redirect
from django.views import View
from .forms import UserLoginRegisterForm, OtpVerifyForm, UserRegisterForm
from .models import OTP, User
from django.utils import timezone
from .services import send_otp_code
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from shortener.models import ShortLink
from django.views.generic import ListView
from django.core.cache import cache


class LoginView(View):
    form_class = UserLoginRegisterForm
    template_name = 'accounts/login.html'


    def dispatch(self, request, *args, **kwargs):
        nxt = request.GET.get('next')
        if nxt:
            request.session['next'] = nxt
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            phone = form.cleaned_data['phone']

            phone_key = f"otp:req:{phone}"
            window = getattr(settings, "OTP_ATTEMPT_WINDOW", 300)
            max_reqs = getattr(settings, "OTP_REQUESTS_PER_WINDOW", 5)

            count = cache.get(phone_key, 0)
            if count >= max_reqs:
                form.add_error('phone', "Too many requests. Please try again later.")
                return render(request, self.template_name, {'form': form})

            cache.set(phone_key, count + 1, timeout=window)

            cooldown = getattr(settings, "OTP_RESEND_COOLDOWN", 120)
            otp = OTP.objects.filter(phone=phone).first()
            if otp:
                elapsed = (timezone.now() - otp.created_at).total_seconds()
                if elapsed < cooldown:
                    form.add_error('phone', f'Please wait {int(cooldown - elapsed)} seconds before trying again')
                    return render(request, self.template_name, {'form': form})
                otp.delete()

            otp = OTP.objects.create(phone=phone, code=OTP.generate_otp(), created_at=timezone.now())
            request.session['login_info'] = {
                'phone': phone,
            }

            ok = send_otp_code(phone, otp.code)
            if ok:
                return redirect("verify_otp")
            else:
                form.add_error(None, "Something went wrong! please try again later.")
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {'form': form})


class LoginVerifyView(View):
    template_name = 'accounts/verify.html'
    form_class = OtpVerifyForm

    def get(self, request):
        form = self.form_class()
        login_info = request.session.get('login_info') or {}
        phone = login_info.get('phone')
        if not phone:
            return redirect('login')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        login_info = request.session.get('login_info') or {}
        phone = login_info.get('phone')
        if not phone:
            return redirect('login')

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        cd = form.cleaned_data
        otp_obj = OTP.objects.filter(phone=phone, code=cd['otp']).first()
        if otp_obj:
            otp_obj.delete()

            if not otp_obj.is_valid():
                form.add_error('otp','This code is Expired')
                return render(request, self.template_name, {'form': form})

            request.session.pop('login_info', None)

            user = User.objects.filter(phone=phone).first()
            if not user:
                new_user = User.objects.create_user(phone=phone)
                login(request, new_user)
                return redirect('complete-register')

            login(request, user)
            next_url = request.session.pop('next', None)
            return redirect(next_url or 'home')

        form.add_error('otp','Invalid Otp')
        return render(request, self.template_name, {'form': form})



class CompleteRegisterView(LoginRequiredMixin, View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        form.save()
        return redirect('home')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home')



class DashboardView(LoginRequiredMixin, ListView):
    model = ShortLink
    template_name = "accounts/dashboard.html"
    context_object_name = "links"
    paginate_by = 10

    def get_queryset(self):
        return ShortLink.objects.filter(owner=self.request.user).order_by("-created_at")