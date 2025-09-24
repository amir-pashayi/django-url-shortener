from django.conf import settings
from kavenegar import *

def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
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