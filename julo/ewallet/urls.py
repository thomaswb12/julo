from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'wallets', views.WalletViewSet, basename='wallets')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
router.register(r'users', views.CustomUserViewSet, basename='users')

router.register(r'v1/wallet', views.WalletView, basename='wallets')

urlpatterns = [
    path('v1/init/', views.LoginView.as_view(), name='login'),
    path('v1/logout/', views.LogoutView.as_view(), name='logout'),
    # path('v1/wallet/', views.WalletView.as_view(), name='enable-wallet'),
    # path('v1/wallet/deposits', views.WalletView.deposits, name='enable-wallet'),
    path('', include(router.urls)),
]
