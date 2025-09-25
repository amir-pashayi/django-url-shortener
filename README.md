# 🔗 URL Shortener (Django)

A clean, production-ready **URL shortener** built with Django.  
Users authenticate via **phone + OTP**, create and manage short links, and track clicks with safe redirects.

---

## ✨ Features
- **OTP authentication** (phone-based) with:
  - Per-phone **rate limiting** (default: 5 requests / 5 min)
  - **Cooldown** between resends (default: 120s)
  - **OTP expiration** (default: 300s)
- **Short link creation** with auto-generated `code`
  - Codes avoid reserved words (e.g. `admin`, `login`, `api`, …)
  - Links expire automatically after 1 year (default)
- **Safe redirect** with **atomic** click counter
- **URL validation**:
  - Only `http://` and `https://`
  - Rejects `javascript:` / `data:`** schemes
  - Rejects links to your own domain
- **User dashboard** to manage your links
- **Bootstrap 5 UI**

---

## 🧩 Architecture
- **Django apps**: `accounts`, `shortener`
- **Auth**: phone + OTP (via Kavenegar, with dev fallback to console)
- **Short link model**: unique `code` (A–Z, a–z, 0–9), reserved list protected
- **Click tracking**: `F()`-based atomic increment
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

| Key | Description | Default |
| --- | ----------- | ------- |
| `SECRET_KEY` | Django secret | **required** |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `KAVENEGAR_API_KEY` | SMS provider key (optional in dev) | empty |
| `OTP_RESEND_COOLDOWN` | Seconds between resends | `120` |
| `OTP_ATTEMPT_WINDOW` | Rate-limit window (seconds) | `300` |
| `OTP_REQUESTS_PER_WINDOW` | Max requests per window | `5` |
| `OTP_EXPIRATION_TIME` | Seconds before OTP expires | `300` |

### 5) Run
```bash
python manage.py migrate
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## 🔐 OTP Flow
1. User enters phone → server generates a 6-digit OTP and stores it.
2. Rate-limiting: max `OTP_REQUESTS_PER_WINDOW` per phone during `OTP_ATTEMPT_WINDOW`.
3. Resend cooldown: `OTP_RESEND_COOLDOWN` seconds.
4. OTP is sent via Kavenegar (if API key present), or logged to console in dev mode.
5. On verify: OTP must be valid and not older than `OTP_EXPIRATION_TIME`.

---

## 🧪 URL Rules & Redirect Safety
- Accepts **http/https** only.
- Rejects **`javascript:`** and **`data:`** schemes.
- Rejects links pointing to your own domain (from `ALLOWED_HOSTS`).
- On redirect: increments `click_count` atomically and checks expiry (returns 404 if expired).

---

## 📦 Project Structure
```
django-url-shortener/
├─ urlshortner/
│  ├─ accounts/      # phone auth, otp
│  ├─ shortener/     # short link logic
│  ├─ templates/     # bootstrap ui
│  ├─ manage.py
├─ requirements.txt
└─ README.md
```

---

## 🔧 Development Tip
On development, with `DEBUG=True` or no `KAVENEGAR_API_KEY`, OTPs are **printed to console** instead of calling the provider:
```
[OTP][DEV] to=09123456789 code=123456
```

---

## 🛡️ Security Notes
- Always set `DEBUG=False` in production.
- Configure `ALLOWED_HOSTS`.
- Consider enabling HSTS, SSL redirect, and secure cookies.
- Keep your `SECRET_KEY` secret; never commit `.env`.

---

## 🧭 Routes
| Path | View | Notes |
| ---- | ---- | ----- |
| `/` | Home | Landing page |
| `/create/` | CreateShortLinkView | Make a short link |
| `/link/<code>/` | LinkDetailView | Details page |
| `/<code>/` | GoView | Redirect to target URL |
| `/accounts/login/` | LoginView | Phone login (OTP) |
| `/accounts/verify/` | LoginVerifyView | Submit OTP |
| `/accounts/dashboard/` | DashboardView | Manage your links |

---
## ❤️ Credits

Developed with ❤️ by **Amir Pashayi**
