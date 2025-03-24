import uuid
from django.db import models
from user.models import User

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Wallet for {self.user.username}"
    
class WalletFunding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=15, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 'success':
            self.wallet.balance += self.amount
            self.wallet.save()
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['created_at']

# amount, description, accName, accNo, bankCode
class Transfer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=15)
    status = models.CharField(max_length=20, null=True, blank=True, default="pending")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.user == self.wallet.user:
            self.balance = self.wallet.balance
            self.wallet.save()
        super().save(*args, **kwargs)


