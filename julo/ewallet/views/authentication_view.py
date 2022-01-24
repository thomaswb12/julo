
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import SignInSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth import authenticate

from drf_expiring_token.authentication import token_expire_handler
from drf_expiring_token.models import ExpiringToken
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        sign_in_serializer = SignInSerializer(data=request.data)
        if not sign_in_serializer.is_valid():
            return Response(sign_in_serializer.errors, status=HTTP_400_BAD_REQUEST)

        print(sign_in_serializer.data['customer_xid'])
        user = authenticate(
            customer_xid=sign_in_serializer.data['customer_xid'],
        )

        if not user:
            return Response({
                'data': {
                    'token': '',
                },
                'status': 'Fail'
            }, status=HTTP_400_BAD_REQUEST)
        # TOKEN STUFF
        token, _ = ExpiringToken.objects.get_or_create(user=user)

        # token_expire_handler will check, if the token is expired it will generate new one
        is_expired, token = token_expire_handler(token)  # The implementation will be described further
        return Response({
            'data': {
                'token': token.key,
            },
            'status': 'Success'
        }, status=HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = {'status': 'Success'}
        request.user.auth_token.delete()
        return Response(content, status=HTTP_200_OK)