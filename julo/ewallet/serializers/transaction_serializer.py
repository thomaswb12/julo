from rest_framework import serializers
from ..models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(source='get_transaction_type_display')
    status_transaction = serializers.CharField(source='get_status_transaction_display')

    class Meta:
        model = Transaction
        fields = '__all__'