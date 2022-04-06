from rest_framework import serializers
from .models import *
from user.models import ContactBook


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactBook
        fields = ["username", "email"]


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amail
        fields = ["sender", "receiver"]
