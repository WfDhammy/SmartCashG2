from wallet.models import Wallet, WalletFunding
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
