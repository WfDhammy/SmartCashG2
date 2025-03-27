from . import views
from django.urls import path


urlpatterns = [
    path('', views.WalletListCreateAPIView.as_view(), name="createWalletList"),
    path('<uuid:id>/', views.WalletDetailAPIView.as_view(), name="Detail"),
    path('fund/', views.FundWallet.as_view(), name="fund"),
    path('fund/all', views.FundWalletView.as_view(), name="createWalletList"),
    path('<uuid:id>/', views.RetrieveFunding.as_view(), name="Detail"),
    path('webhook/', views.WebHook.as_view(), name="webhook"),
    path('transfer/', views.TransferAction.as_view(), name="transfer"),
]