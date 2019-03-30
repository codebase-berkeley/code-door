from django.db import models
from codedoor.models import Profile

# Create your models here.


class TransactionRecord(models.Model):
    sender = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Transaction:{}: {} --> {} {} codebucks>".format(
            self.created_at, self.sender, self.recipient, self.amount
        )
