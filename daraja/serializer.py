from rest_framework import serializers
from django.core.exceptions import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField

from daraja.models import Transaction

class MakePaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    phone_number = serializers.CharField()
    
    def validate_phone_number(self, phone_number):
        if phone_number[0] == "+":
            phone_number = phone_number[1:]
        if phone_number[0] == "0":
            phone_number = "254" + phone_number[1:]

        return phone_number

    def validate_amount(self, amount):
        if not amount or float(amount) <= 0:
            raise serializers.ValidationError(
                {"error": "Amount must be greater than Zero"}
            )
        return amount


class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
        )

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"