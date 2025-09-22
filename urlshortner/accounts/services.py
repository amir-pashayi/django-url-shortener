import os
from kavenegar import KavenegarAPI

def send_otp_code(phone, code):
    api = KavenegarAPI(os.environ["KAVENEGAR_API_KEY"])
    params = {'receptor': phone, 'template': 'django-ec', 'token': code, 'type': 'sms'}
    return api.verify_lookup(params)