from django.shortcuts import render, redirect
from django.views import View
from .forms import ShortenForm
from .models import ShortLink
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404



class HomeView(View):
    template_name = "shortener/home.html"

    def get(self, request):
        links = None
        if request.user.is_authenticated:
            links = ShortLink.objects.filter(owner=request.user).order_by("-created_at")[:5]
        return render(request, self.template_name, {"links": links})


class CreateShortLinkView(LoginRequiredMixin, View):
    template_name = 'shortener/create.html'
    form_class = ShortenForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ShortenForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            original_url = cd['original_url']
            code = ShortLink.generate_unique_code()
            expires_at = timezone.now() + timedelta(days=365)
            link = ShortLink.objects.create(
                owner=request.user,
                original_url=original_url,
                code=code,
                expires_at=expires_at,
            )

            return redirect("link_detail", code=link.code)



class LinkDetailView(LoginRequiredMixin, View):
    template_name = "shortener/detail.html"

    def get(self, request, code):
        link = get_object_or_404(ShortLink, code=code, owner=request.user)
        return render(request, self.template_name, {"link": link})