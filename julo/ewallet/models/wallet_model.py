from django.db import models
import uuid
from .abstract_model import CommonInfo

class Wallet(CommonInfo):
    STATUS_CHOICES =( 
        (True, "enabled"), 
        (False, "disabled"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)
    balance = models.FloatField(default=0)
    owned_by = models.OneToOneField('CustomUser', on_delete=models.CASCADE, db_constraint=False)
    enabled_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)