from django import forms

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
        return url
