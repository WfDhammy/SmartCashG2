from django.contrib import admin
from .models import Wallet, WalletFunding, Transfer


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance', 'created_at']


class WalletFundingAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'user', 'amount', 'reference', 'status', 'created_at']

class TransferAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'description', 'account_name', 'account_number', 'bank_code', 'status', 'balance', 'reference', 'created_at']
    list_filter = ['status', 'created_at', 'user']
    search_fields = ['user__email', 'account_name', 'account_number', 'reference']
    list_editable = ['status', 'amount', 'description']
    

    



admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(WalletFunding, WalletFundingAdmin)


