from rest_framework import serializers
from .models import Exchange


class ExchangeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'