import json
import requests
from requests.exceptions import ConnectionError
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from phonenumber_field.phonenumber import PhoneNumber
from account.models import Points

User = get_user_model()

from daraja.generate_token import generate_token
from daraja.encode_token import encode_token
from daraja.format_date import format_date
from daraja.serializer import MakePaymentSerializer, TransactionSerializer
from daraja.models import Transaction, Savings

# Create your views here.
class InitiateSTKPush(GenericAPIView):
    serializer_class = MakePaymentSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        phone_number = serializer.validated_data['phone_number']

        paymentResponse = self.initiate_stk_push(amount, phone_number)
        return Response(paymentResponse)

    def initiate_stk_push(self, amount, phone_number) -> dict:
        access_token = generate_token()

        if access_token is None:
            return {'errors': ['Failed to generate access token']}

        timestamp = format_date()
        password = encode_token(timestamp)

        payload = {
        "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": 9713209,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://chamayettu.co.ke/api/v1/mpesa/callback/",
        "AccountReference": "Chama Yetu Online Payment",
        "TransactionDesc": "Contribution"
        }

        headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
        }


        response = requests.post(settings.API_RESOURCE_URL, json=payload, headers=headers)
       
        response_text = response.text
        response_json = json.loads(response_text)

        if 'errorCode' in response_json:
            data = {'errors': [response_json['errorMessage']]}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        merchant_request_id = response_json['MerchantRequestID']
        checkout_request_id = response_json['CheckoutRequestID']
        response_code = response_json['ResponseCode']
        response_description = response_json['ResponseDescription']
        customer_message = response_json['CustomerMessage']

        data = {
            'data': {
                'MerchantRequestID': merchant_request_id,
                'CheckoutRequestID': checkout_request_id,
                'ResponseCode': response_code,
                'ResponseDescription': response_description,
                'CustomerMessage': customer_message
            }
        }

        save_data = {
            "phone_number": phone_number,
            "amount": amount,
            "description": response_description,
            "checkout_request_id": checkout_request_id,
        }

        Transaction.objects.create(**save_data)


        data = {
            'data': {
                'MerchantRequestID': merchant_request_id,
                'CheckoutRequestID': checkout_request_id,
                'ResponseCode': response_code,
                'ResponseDescription': response_description,
                'CustomerMessage': customer_message
            }
        }

        return data

# Handle callback
class STKPushCallback(GenericAPIView):
    def get_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            status = 1 
        return status

    def get_transaction_object(self, data):
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        transaction, _ = Transaction.objects.get_or_create(
            checkout_request_id=checkout_request_id
        )

        return transaction

    def handle_successful_pay(self, data, transaction):
        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        description = data["Body"]["stkCallback"]["ResultDesc"]

        for item in items:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                receipt_no = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]

        transaction.amount = amount
        transaction.phone_number = PhoneNumber(raw_input=phone_number)
        transaction.receipt_no = receipt_no
        transaction.is_confirmed = True
        transaction.description = description

        new_phone_number = "+" + str(phone_number)
        user = User.objects.get(phone_number=new_phone_number)

        points = Points.objects.get(user=user)
        points.points += int(amount) / 100

        points.save()

        return transaction
    
    def callback_handler(self, data):
        status = self.get_status(data)
        transaction = self.get_transaction_object(data)
        if status==0:
            self.handle_successful_pay(data, transaction)
        else:
            description = data["Body"]["stkCallback"]["ResultDesc"]
            transaction.status = 1
            transaction.description = description
            transaction.is_confirmed = True

        transaction.status = status
        transaction.save()

        return Response({"status": "ok", "code": 0}, status=200)
        
    def get(self, request):
        return Response({"status": "OK"}, status=200)

    def post(self, request):
        data = request.data
        self.callback_handler(data)
        return self.callback_handler(data)


class TransactionView(GenericAPIView):
    serializer_class = TransactionSerializer
    def get(self, request, id):
        transaction = Transaction.objects.get(checkout_request_id=id)
        
        if transaction.is_confirmed:
            if transaction.status == 0:
                description = "Payment Successful"
                return Response({"status": "ok", "code": 0, "description": description}, status=200)

            elif transaction.status == 1:
                return Response({"status": "errors", "code": 1, "description": transaction.description}, status=200)
            else:
                return Response({"status": "errors", "code": transaction.status, "description": transaction.description}, status=200)
            
        return Response({"status": "errors", "code": 1, "description": "pending"}, status=200)

class InitiateSTKPushSavings(GenericAPIView):
    serializer_class = MakePaymentSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        phone_number = serializer.validated_data['phone_number']

        paymentResponse = self.initiate_stk_push(amount, phone_number)

        return Response(paymentResponse)

    def initiate_stk_push(self, amount, phone_number) -> dict:
        access_token = generate_token()

        if access_token is None:
            return {'errors': ['Failed to generate access token']}

        timestamp = format_date()
        password = encode_token(timestamp)

        payload = {
        "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": 9713209,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://chamayettu.co.ke/api/v1/mpesa/savings/callback/",
        "AccountReference": "Chama Yetu Online Payment",
        "TransactionDesc": "Contribution"
        }

        headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
        }

        response = requests.post(settings.API_RESOURCE_URL, json=payload, headers=headers)

        response_text = response.text
        response_json = json.loads(response_text)

        if 'errorCode' in response_json:
            return {'errors': [response_json['errorMessage']]}

        merchant_request_id = response_json['MerchantRequestID']
        checkout_request_id = response_json['CheckoutRequestID']
        response_code = response_json['ResponseCode']
        response_description = response_json['ResponseDescription']
        customer_message = response_json['CustomerMessage']

        data = {
            'data': {
                'MerchantRequestID': merchant_request_id,
                'CheckoutRequestID': checkout_request_id,
                'ResponseCode': response_code,
                'ResponseDescription': response_description,
                'CustomerMessage': customer_message
            }
        }

        new_phone_number = "+" + str(phone_number)
        user = User.objects.get(phone_number=new_phone_number)
        
        save_data = {
            "user": user,
            "phone_number": phone_number,
            "amount": amount,
            "description": response_description,
            "checkout_request_id": checkout_request_id,
        }

        Savings.objects.create(**save_data)

        data = {
            'data': {
                'MerchantRequestID': merchant_request_id,
                'CheckoutRequestID': checkout_request_id,
                'ResponseCode': response_code,
                'ResponseDescription': response_description,
                'CustomerMessage': customer_message
            }
        }

        return data

# Handle callback
class STKPushCallbackSavings(GenericAPIView):
    def get_status(self, data):
        try:
            status = data["Body"]["stkCallback"]["ResultCode"]
        except Exception as e:
            status = 1 
        return status

    def get_savings_object(self, data):
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        savings, _ = Savings.objects.get_or_create(
            checkout_request_id=checkout_request_id
        )

        return savings

    def handle_successful_pay(self, data, savings):
        items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        description = data["Body"]["stkCallback"]["ResultDesc"]

        for item in items:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                receipt_no = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]
                
        savings.amount = amount
        savings.phone_number = PhoneNumber(raw_input=phone_number)
        savings.receipt_no = receipt_no
        savings.is_confirmed = True
        savings.description = description

        new_phone_number = "+" + str(phone_number)
        user = User.objects.get(phone_number=new_phone_number)

        points = Points.objects.get(user=user)
        points.points += int(amount) / 100

        points.save()

        return savings
    
    def callback_handler(self, data):
        status = self.get_status(data)
        savings = self.get_savings_object(data)
        if status==0:
            self.handle_successful_pay(data, savings)
        else:
            description = data["Body"]["stkCallback"]["ResultDesc"]
            savings.status = 1
            savings.description = description
            savings.is_confirmed = True

        savings.status = status
        savings.save()

        return Response({"status": "ok", "code": 0}, status=200)
        
    def get(self, request):
        return Response({"status": "OK"}, status=200)

    def post(self, request):
        data = request.data
        self.callback_handler(data)
        return self.callback_handler(data)


class TransactionViewSavings(GenericAPIView):
    serializer_class = TransactionSerializer
    def get(self, request, id):
        savings = Savings.objects.get(checkout_request_id=id)
        
        if savings.is_confirmed:
            if savings.status == 0:
                description = "Payment Successful"
                return Response({"status": "ok", "code": 0, "description": description}, status=200)

            elif savings.status == 1:
                return Response({"status": "errors", "code": 1, "description": savings.description}, status=200)
            else:
                return Response({"status": "errors", "code": savings.status, "description": savings.description}, status=200)
            
        return Response({"status": "errors", "code": 1, "description": "pending"}, status=200)