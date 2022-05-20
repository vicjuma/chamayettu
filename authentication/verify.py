import os
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)

def send(phone_number):
    try:
        return verify.verifications.create(to=phone_number, channel='sms')
    except TwilioRestException as e:
        return None

def check(phone_number, code):
    try:
        result = verify.verification_checks.create(to=phone_number, code=code)
    except TwilioRestException:
        return False

    return result.status == 'approved'

    