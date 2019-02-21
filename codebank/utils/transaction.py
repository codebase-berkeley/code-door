from codedoor.models import Profile
from django.contrib.auth.models import User
from django.db import transaction
import random

class TransactionError(Exception):
    msg = "We couldn't complete your transaction because it is invalid."

class MinimumAmountError(TransactionError):
    """
    Raise when a transaction (e.g. a send) is below the minimum amount.
    """
    def __init__(self, msg):
        self.msg = msg

class OverdraftError(TransactionError):
    """
    Raise when the sender does not have enough money to complete the transaction.
    """
    def __init__(self, msg):
        self.msg = msg

class InvalidRecipientError(TransactionError):
    """
    Raise when the recipient profile is missing or invalid.
    """
    def __init__(self, msg):
        self.msg = msg

def send_codebucks(sender_email, recipient_email, amount):
    """
    :param sender: Profile of the sender.
    :param recipient: Profile of the recipient.
    :param amount: Positive integer amount to send.
    :return: True if the transaction completed successfully, else False
    """
    with transaction.atomic():
        sender = Profile.objects.select_for_update().get(user=User.objects.get(email=sender_email))
        recipient = Profile.objects.select_for_update().get(user=User.objects.get(email=recipient_email))
        if not recipient:
            raise InvalidRecipientError("It looks like the recipient doesn't have an account.")
        if sender and sender != recipient:
            if amount < 100:
                raise MinimumAmountError("The minimum transaction is 100 codebucks.")
            elif sender.codebucks < amount:
                raise OverdraftError("You don't have enough codebucks in your account to complete that transaction.")
            sender.codebucks -= amount
            recipient.codebucks += amount
            sender.save()
            recipient.save()
        else:
            raise TransactionError()

def coinflip(email, amount):
    with transaction.atomic():
        profile = Profile.objects.select_for_update().get(user=User.objects.get(email=email))
        if profile.codebucks < amount:
            raise OverdraftError("You don't have enough codebucks to wager.")
        elif amount < 100:
            raise MinimumAmountError("The gambling committee requires a minimum wager of at least 100 codebucks.")

        if random.random() < 0.49:
            amount = amount * -1
        profile.codebucks += amount
        profile.save()
        return amount
