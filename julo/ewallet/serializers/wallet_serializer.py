from rest_framework import serializers
from ..models import Wallet, Transaction
from rest_framework.validators import UniqueValidator

class WalletSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    
    class Meta:
        model = Wallet
        fields = '__all__'

class UpdateWalletSerializer(serializers.Serializer):
    is_disabled = serializers.BooleanField()

    def validate_is_disabled(self, value):
        if not value:
            raise serializers.ValidationError("This field is required and value must be true")
        return value

class WithdrawalDepositWalletSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=1)
    reference_id = serializers.UUIDField(validators=[UniqueValidator(queryset=Transaction.objects.all())])