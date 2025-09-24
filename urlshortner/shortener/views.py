from django.shortcuts import render, redirect
from django.views import View
from .forms import ShortenForm
from .models import ShortLink
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import F
from django.db import IntegrityError, transaction



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
            try:
                with transaction.atomic():
                    link = ShortLink.objects.create(
                        owner=request.user,
                        original_url=original_url,
                        code=code,
                        expires_at=expires_at,
                    )
                return redirect("link_detail", code=link.code)
            except IntegrityError:
                form.add_error(None, "Something went wrong. Please try again.")
                return render(request, self.template_name, {"form": form})




class LinkDetailView(LoginRequiredMixin, View):
    template_name = "shortener/detail.html"

    def get(self, request, code):
        link = get_object_or_404(ShortLink, code=code, owner=request.user)
        return render(request, self.template_name, {"link": link})


class GoView(View):
    def get(self, request, code):
        link = get_object_or_404(ShortLink, code=code, is_active=True)
        if link.expires_at and timezone.now() > link.expires_at:
            raise Http404("Link expired")
        ShortLink.objects.filter(pk=link.pk).update(click_count=F('click_count') + 1)
        return redirect(link.original_url)



class LinkToggleActiveView(LoginRequiredMixin, View):
    def post(self, request, code):
        link = get_object_or_404(ShortLink, code=code, owner=request.user)
        link.is_active = not link.is_active
        link.save(update_fields=['is_active'])
        return redirect('link_detail', code=link.code)
