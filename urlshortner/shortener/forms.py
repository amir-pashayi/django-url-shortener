from django import forms
from urllib.parse import urlparse
from django.conf import settings

class ShortenForm(forms.Form):
    original_url = forms.URLField(
        label="URL",
        widget=forms.URLInput(attrs={"placeholder": "https://example.com"})
    )

    def clean_original_url(self):
        url = (self.cleaned_data["original_url"] or "").strip()

        if not (url.startswith("http://") or url.startswith("https://")):
            raise forms.ValidationError("URL must start with http or https.")

        if url.lower().startswith(("javascript:", "data:")):
            raise forms.ValidationError("Unsupported URL scheme.")

        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()

        reserved_hosts = {h.lower() for h in getattr(settings, "ALLOWED_HOSTS", []) if h and h != "*"}
        reserved_hosts |= {"localhost", "127.0.0.1"}

        if hostname in reserved_hosts:
            raise forms.ValidationError("You cannot shorten links from this domain.")
        return url
