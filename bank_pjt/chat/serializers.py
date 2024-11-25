# chat/serializers.py

from rest_framework import serializers
from .models import StandardizedTermDeposit

class StandardizedTermDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandardizedTermDeposit
        fields = '__all__'
