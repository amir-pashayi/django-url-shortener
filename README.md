# 🔗 URL Shortener (Django)

A clean, production-leaning **URL shortener** built with Django.  
Users authenticate via **phone + OTP**, create and manage short links, and track clicks with safe redirects.

---

## ✨ Features
- **OTP auth** (phone-based) with:
  - per-phone **rate limiting** (default: 5 requests / 5 min) and **cooldown** between resends
  - OTP **expiration** (default: 5 min)
- **Create** short links (auto-generated `code`), **activate/deactivate**, **expire** after 1 year (default)
- **Safe redirect** with **atomic** click counter
- **URL validation**: http/https only, **blocks** `javascript:` / `data:` schemes, **blocks own domain**
- **User dashboard** of links
- Bootstrap 5 UI

---

## 🧩 Architecture
- **Django apps**: `accounts`, `shortener`
- **Auth**: phone + OTP (Kavenegar)
- **Short link model**: unique `code` (A–Z, a–z, 0–9), reserved words protected
- **Click tracking**: `F()`-based atomic increment during redirect
- **Templates**: Bootstrap 5

---

## 🚀 Quickstart

### 1) Clone & enter
```bash
git clone https://github.com/amir-pashayi/django-url-shortener.git
cd django-url-shortener/urlshortner
```

### 2) Python env
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r ../requirements.txt
```

### 4) Environment variables
Copy the example and adjust:
```bash
cp .env.example .env
```

| Key | Description | Example |
| --- | --- | --- |
| `SECRET_KEY` | Django secret | use a strong random value |
| `ALLOWED_HOSTS` | Allowed hosts | `["localhost", "127.0.0.1"]` or `["yourdomain.com"]` |
| `KAVENEGAR_API_KEY` | (Optional) SMS provider key for OTP | `xxxxxxxx` |

> On development you can leave `KAVENEGAR_API_KEY` empty and log OTP in console if you enable a failsafe. (See **Development Tip** below.)

### 5) Run
```bash
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## 🔐 OTP Flow (Overview)
1. User enters phone → server generates 6-digit OTP and stores it.
2. Server **rate-limits** OTP requests per phone (default: 5 / 5min) and enforces resend **cooldown** (default: 120s).
3. OTP is sent via Kavenegar (or logged to console on dev if you enable a failsafe).
4. User enters OTP → if valid and within **expiration** (default: 300s), session is authenticated.

**Config knobs (typical):**
- `OTP_ATTEMPT_WINDOW` (seconds, default 300)
- `OTP_REQUESTS_PER_WINDOW` (default 5)
- `OTP_RESEND_COOLDOWN` (seconds, default 120)
- `OTP_EXPIRATION_TIME` (seconds, default 300)

> Adjust these in `settings.py` or via `.env` if you’ve wired them to env vars.

---

## 🧪 URL Rules & Redirect Safety
- Accepts **http**/**https** only
- Rejects **`javascript:`** and **`data:`** schemes
- Rejects links pointing to **your own domain** (from `ALLOWED_HOSTS`)
- On redirect: increments `click_count` **atomically** and checks **expiry** (returns 404 if expired)

---

## 📦 Project Structure (trimmed)
```
django-url-shortener/
├─ urlshortner/
│  ├─ accounts/
│  ├─ shortener/
│  ├─ templates/
│  ├─ manage.py
├─ requirements.txt
└─ README.md
```

---

## 🔧 Development Tip (OTP failsafe)
For a smooth local experience, make the OTP sender **fallback to console** when `DEBUG=True` or `KAVENEGAR_API_KEY` is empty. Example:

```python
# accounts/services.py (example)
from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException

def send_otp_code(phone, code) -> bool:
    api_key = getattr(settings, "KAVENEGAR_API_KEY", "") or ""
    if getattr(settings, "DEBUG", False) or not api_key:
        print(f"[OTP][DEV] to={{phone}} code={{code}}")
        return True
    try:
        api = KavenegarAPI(api_key)
        api.verify_lookup({{"receptor": phone, "template": "django-ec", "token": code}})
        return True
    except (APIException, HTTPException) as e:
        print(f"[OTP][ERR] {{e}}")
        return False
```

---

## 🛡️ Security Notes
- Set `DEBUG=False` and **configure `ALLOWED_HOSTS`** in production.
- Consider enabling secure cookies, HSTS, and SSL redirect for real deployments.
- Keep your `SECRET_KEY` safe; never commit `.env`.

---

## 🧭 Routes (UI)
| Path | View | Notes |
| --- | --- | --- |
| `/` | Home | New link CTA + recent links |
| `/create/` | CreateShortLinkView | Create a short link |
| `/link/<code>/` | LinkDetailView | Details page with copy button |
| `/<code>/` | GoView | Redirect to original URL |
| `/accounts/login/` | LoginView | Phone-based login (OTP) |
| `/accounts/verify/` | LoginVerifyView | Submit OTP |
| `/accounts/dashboard/` | DashboardView | Your links |

---

## 📄 License
Not specified. If you plan to open source, consider adding a license file (MIT/Apache-2.0, etc.).
