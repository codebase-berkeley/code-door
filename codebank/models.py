from django.db import models
from codedoor.models import Profile

# Create your models here.


class TransactionRecord(models.Model):
    sender = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="sender_set")
    recipient = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name="recipient_set")
    amount = models.IntegerField(default=0)
    note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Transaction:{}: {} --> {} {} codebucks with note: {}>".format(
            self.created_at, self.sender, self.recipient, self.amount, self.note
        )
