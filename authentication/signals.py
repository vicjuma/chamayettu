from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views import View
from daraja.models import Savings

import os
from django.conf import settings

MESSAGE = ""

@receiver(post_save, sender=Savings)
def create_savings(sender, instance, created, **kwargs):
    global MESSAGE
    
    if created:
        # blur the middle digits of the phone number
        phone_number = str(instance.phone_number)
        phone_number = phone_number[:6] + "***" + phone_number[-3:]

        message = f"{phone_number} has saved {instance.amount}"
        MESSAGE = message
        
        # write MESSAGE to a file in BASE_DIR
        with open(f"{settings.BASE_DIR}/message.txt", "w") as f:
            f.write(message)

        f.close()

class MessageView(View):
    MESSAGE
    def get(self, request):
        msg = ""

        # read MESSAGE from a file in BASE_DIR
        if os.path.exists(f"{settings.BASE_DIR}/message.txt"):
            with open(f"{settings.BASE_DIR}/message.txt", "r") as f:
                msg = f.read()

            f.close()
        
        return JsonResponse({"message": msg})
