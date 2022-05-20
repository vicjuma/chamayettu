import base64
from django.conf import settings

def encode_token(dates):
    data = settings.BUSINESS_SHORT_CODE + settings.PASS_KEY + dates
    encode_data = base64.b64encode(data.encode('utf-8'))
    decode_data = encode_data.decode('utf-8')
    return decode_data

