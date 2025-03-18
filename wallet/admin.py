from django.contrib import admin
from .models import Wallet, WalletFunding


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance', 'created_at']


class WalletFundingAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'user', 'amount', 'reference', 'status', 'created_at']


admin.site.register(Wallet, WalletAdmin)

admin.site.register(WalletFunding, WalletFundingAdmin)


