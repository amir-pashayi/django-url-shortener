from django.conf import settings
from kavenegar import *

def send_otp_code(phone_number, code):
	try:
		api_key = settings.KAVENEGAR_API_KEY
		if getattr(settings, "DEBUG", False) or not api_key:
			print(f"[OTP][DEV] to={phone_number} code={code}")
			return True

		api = KavenegarAPI(api_key)
		params = {
			'receptor': phone_number,
            'template': 'django-ec',
            'token': code,
		}
		api.verify_lookup(params)
		return True

	except (APIException, HTTPException) as e:
		print(f"[OTP][ERR] provider_error={e} phone={phone_number}")
		return False