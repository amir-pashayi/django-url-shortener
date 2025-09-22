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
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)