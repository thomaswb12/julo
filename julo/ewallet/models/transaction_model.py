from django.db import models
import uuid
from .abstract_model import CommonInfo

class Transaction(CommonInfo):
    TYPE_TRANSACTION = (
        ('0', 'DEACTIVATE'),
        ('1', 'ACTIVATE'),
        ('2', 'DEPOSIT'),
        ('3', 'WITHDRAWAL'),
        ('4', 'TRANSFER IN'),
        ('5', 'TRANSFER OUT'),
        ('6', 'TRANSACTION IN'),
        ('7', 'TRANSACTION OUT'),
    )

    STATUS_TRANSACTION = (
        ('0', 'PROGRESS'),
        ('1', 'CANCELLED'),
        ('2', 'SUCCESS'),
    )

    action_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_constraint=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(default=0)
    transaction_type = models.CharField(choices=TYPE_TRANSACTION, max_length=255, blank=True)
    reference_id = models.UUIDField(unique=True, blank=True, null=True)
    status_transaction = models.CharField(choices=STATUS_TRANSACTION, max_length=255, blank=True)
    wallet_source = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                  related_name="wallet_source", db_constraint=False, blank=True, null=True)
    wallet_destination = models.ForeignKey('Wallet', on_delete=models.CASCADE,
                                  related_name="wallet_destination", db_constraint=False, blank=True, null=True)
