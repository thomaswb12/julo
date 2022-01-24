from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Wallet, Transaction
from ..serializers import WalletSerializer, UpdateWalletSerializer, WithdrawalDepositWalletSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.decorators import action


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        status = "success"
        data = {}
        response_code = HTTP_200_OK
        message = "success get wallet info"

        try:
            wallet = request.user.wallet
            if not wallet.status:
                status = "fail"
                data = {}
                response_code = HTTP_400_BAD_REQUEST
                message = "wallet inactive"
            else:
                data = WalletSerializer(wallet).data
        except ObjectDoesNotExist:
            status = "fail"
            data = {}
            response_code = HTTP_404_NOT_FOUND
            message = "wallet not found"

        return Response({
            "status": status,
            "data": {
                "wallet": data
            },
            "message" : message
        }, response_code)

    def create(self, request):
        status = "success"
        data = {}
        response_code = HTTP_200_OK
        time_now = timezone.now()
        message = "success enable wallet"

        try:
            wallet = request.user.wallet
            if wallet.status:
                status = "fail"
                data = {}
                response_code = HTTP_400_BAD_REQUEST
                message = "wallet already active"
            else:
                wallet.status = True
                wallet.enabled_at = time_now
                new_transaction = Transaction(
                    transaction_type = '1',
                    status_transaction = '2',
                    wallet_source = wallet,
                    created_at = time_now,
                    updated_at = time_now,
                    action_by = request.user,
                )

                new_transaction.save()
                wallet.save()
                data = WalletSerializer(wallet).data
        except ObjectDoesNotExist:
            new_wallet = Wallet(
                status = True,
                owned_by = request.user,
                enabled_at = time_now,
                created_at = time_now,
                updated_at = time_now,
            )
            new_transaction = Transaction(
                transaction_type = '1',
                status_transaction = '2',
                wallet_source = new_wallet,
                created_at = time_now,
                updated_at = time_now,
                action_by = request.user,
            )
            new_wallet.save()
            new_transaction.save()
            data = WalletSerializer(new_wallet).data
            message = "success create and enable wallet"
        return Response({
            "status": status,
            "data": {
                "wallet": data
            },
            "message" : message
        }, response_code)

    def patch(self, request, pk=None):
        status = "success"
        data = {}
        response_code = HTTP_200_OK
        update_wallet_serializer = UpdateWalletSerializer(data=request.data)
        time_now = timezone.now()
        message = "success disable wallet"

        if not update_wallet_serializer.is_valid():
            status = "fail"
            response_code = HTTP_400_BAD_REQUEST
            message = update_wallet_serializer.errors
        else:
            try:
                wallet = request.user.wallet
                if wallet.status and update_wallet_serializer.data['is_disabled']:
                    wallet.status = False
                    wallet.disabled_at = time_now

                    new_transaction = Transaction(
                        transaction_type = '0',
                        status_transaction = '2',
                        wallet_source = wallet,
                        created_at = time_now,
                        updated_at = time_now,
                        action_by = request.user,
                    )

                    wallet.save()
                    new_transaction.save()
                    data = WalletSerializer(wallet).data
                else:
                    status = "fail"
                    response_code = HTTP_400_BAD_REQUEST
                    message = "wallet already inactive"
            except ObjectDoesNotExist:
                status = "fail"
                data = {}
                response_code = HTTP_404_NOT_FOUND

        return Response({
            "status": status,
            "data": {
                "wallet": data
            },
            "message" : message
        }, response_code)

    def destroy(self, request, pk=None):
        pass
    
    @action(detail=False, methods=['post'])
    def deposits(self, request, format=None):
        status = "success"
        data = {}
        response_code = HTTP_200_OK
        deposit_wallet_serializer = WithdrawalDepositWalletSerializer(data=request.data)
        time_now = timezone.now()
        message = "success deposit"

        if not deposit_wallet_serializer.is_valid():
            status = "fail"
            response_code = HTTP_400_BAD_REQUEST
            message = deposit_wallet_serializer.errors
        else:
            try:
                wallet = request.user.wallet
                if wallet.status:
                    wallet.balance = wallet.balance + deposit_wallet_serializer.data['amount']
                    new_transaction = Transaction(
                        transaction_type = '2',
                        status_transaction = '2',
                        wallet_source = wallet,
                        created_at = time_now,
                        updated_at = time_now,
                        action_by = request.user,
                        reference_id = deposit_wallet_serializer.data['reference_id'],
                        amount = deposit_wallet_serializer.data['amount']
                    )

                    wallet.save()
                    new_transaction.save()
                    data = {
                        "id": new_transaction.id,
                        "deposited_by": str(new_transaction.action_by),
                        "status": "success",
                        "deposited_at": time_now,
                        "amount": deposit_wallet_serializer.data['amount'],
                        "reference_id": deposit_wallet_serializer.data['reference_id']
                    }
                else:
                    status = "fail"
                    response_code = HTTP_400_BAD_REQUEST
                    message = "wallet inactive"
            except ObjectDoesNotExist:
                status = "fail"
                data = {}
                response_code = HTTP_404_NOT_FOUND
                message = "wallet not found"

        return Response({
            "status": status,
            "data": {
                "deposit": data
            },
            "message" : message
        }, response_code)
    
    @action(detail=False, methods=['post'])
    def withdrawals(self, request, format=None):
        status = "success"
        data = {}
        response_code = HTTP_200_OK
        withdrawal_wallet_serializer = WithdrawalDepositWalletSerializer(data=request.data)
        time_now = timezone.now()
        message = "success withdrawal"

        if not withdrawal_wallet_serializer.is_valid():
            status = "fail"
            response_code = HTTP_400_BAD_REQUEST
            message = withdrawal_wallet_serializer.errors
        else:
            try:
                wallet = request.user.wallet
                if wallet.status and wallet.balance >= withdrawal_wallet_serializer.data['amount']:
                    wallet.balance = wallet.balance - withdrawal_wallet_serializer.data['amount']
                    new_transaction = Transaction(
                        transaction_type = '3',
                        status_transaction = '2',
                        wallet_source = wallet,
                        created_at = time_now,
                        updated_at = time_now,
                        action_by = request.user,
                        reference_id = withdrawal_wallet_serializer.data['reference_id'],
                        amount = -withdrawal_wallet_serializer.data['amount']
                    )

                    wallet.save()
                    new_transaction.save()
                    data = {
                        "id": new_transaction.id,
                        "withdrawn_by": str(new_transaction.action_by),
                        "status": "success",
                        "withdrawn_at": time_now,
                        "amount": -withdrawal_wallet_serializer.data['amount'],
                        "reference_id": withdrawal_wallet_serializer.data['reference_id']
                    }
                else:
                    status = "fail"
                    response_code = HTTP_400_BAD_REQUEST
                    message = "wallet inactive or balance insufficient"
            except ObjectDoesNotExist:
                status = "fail"
                data = {}
                response_code = HTTP_404_NOT_FOUND
                message = "wallet not found"

        return Response({
            "status": status,
            "data": {
                "withdrawal": data
            },
            "message" : message
        }, response_code)