

from django.dispatch import receiver

from byro.bookkeeping.signals import process_transaction
from byro_automatch.automatch import transaction


@receiver(process_transaction)
def on_process_transaction(sender, **kwargs):
    return transaction.process(sender)

