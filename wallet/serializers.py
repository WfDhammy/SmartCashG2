from wallet.models import Wallet, WalletFunding, Transfer
from user.models import User
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletFundingSerializer(serializers.ModelSerializer): 
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    wallet = serializers.SlugRelatedField(slug_field='id', queryset=Wallet.objects.all())

    class Meta:
        model = WalletFunding
        fields = ['id', 'user', 'wallet', 'amount', 'reference', 'created_at', 'status']
        read_only_fields = ['id', 'created_at', 'status']


class TransferSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(slug_field='id', queryset=Wallet.objects.all())
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())
    class Meta:
        model = Transfer
        fields = ['id', 'user', 'status', 'wallet', 'balance', 'amount', 'description', 'account_name', 'account_number', 'bank_code', 'reference', 'created_at']
        read_only_fields = ['id', 'created_at', 'status', 'balance', 'reference']
