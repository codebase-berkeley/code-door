from codedoor.models import Profile
from django.db import transaction
import random
from .slack import get_profile

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

def send_codebucks(sender, recipient, amount):
    """
    :param sender: Profile of the sender.
    :param recipient: Profile of the recipient.
    :param amount: Positive integer amount to send.
    :return: True if the transaction completed successfully, else False
    """
    if not recipient:
        raise InvalidRecipientError("It looks like the recipient doesn't have an account.")
    if sender and sender != recipient:
        if amount < 100:
            raise MinimumAmountError("The minimum transaction is 100 codebucks.")
        elif sender.codebucks < amount:
            raise OverdraftError("You don't have enough codebucks in your account to complete that transaction.")
        with transaction.atomic():
            sender.codebucks -= amount
            recipient.codebucks += amount
            sender.save()
            recipient.save()
    raise TransactionError()

def coinflip(profile, amount):
    if profile.codebucks < amount:
        raise OverdraftError("You don't have enough codebucks to wager.")
    elif amount < 100:
        raise MinimumAmountError("The gambling committee requires a minimum wager of at least 100 codebucks.")

    if random.random() < 0.49:
        amount = amount * -1
    with transaction.atomic():
        profile.codebucks += amount
        profile.save()
    return amount
