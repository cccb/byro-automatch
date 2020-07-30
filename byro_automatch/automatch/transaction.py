"""
Automatch Transaction Handler
"""

from django.db.models import Count

from byro.bookkeeping.models import (
    Transaction,
    RealTransactionSource,
    Booking,
)


def process(transaction):
    """
    Create bookings to balance a transaction.

    The behaviour model must have been trained
    using supervised positive only sample datasets.
    """
    if transaction.is_read_only:
        print("Skipping read-only transaction: {}".format(transaction))
        return None

    if transaction.bookings.count() > 1:
        print("Skipping processed transaction: {}".format(transaction))
        return None


    # Let's query our association layer and 'remember'
    # what we did last time.
    balanced = find_balanced(transaction)
    if not balanced:
        print("No previously balanced transaction found for: {}".format(
            transaction))
        return None

    # We found something we can work with
    for tmpl in template_bookings(balanced):
        booking = clone_booking(transaction, tmpl)
        booking.save()

    print("Processed transaction: {}".format(transaction))
    return transaction


def template_bookings(transaction):
    """Find blancing bookings"""
    return transaction.bookings.exclude(member=None)


def clone_booking(transaction, tmpl):
    """Create a new booking"""
    return Booking(
        transaction=transaction,
        amount=tmpl.amount,
        member=tmpl.member,
        debit_account=tmpl.debit_account,
        credit_account=tmpl.credit_account,
        booking_datetime=transaction.value_datetime)


def find_balanced(transaction):
    """Providing a template, match the last processed transaction."""
    booking = transaction.bookings.first()
    return Transaction.objects \
        .annotate(Count("bookings")) \
        .filter(
            bookings__count__gt=1,
            bookings__amount=booking.amount,
            bookings__memo=booking.memo) \
        .distinct() \
        .order_by("-pk") \
        .first()


def process_all():
    """Process all unbalanced"""
    transactions = Transaction.objects \
        .annotate(Count("bookings")) \
        .filter(bookings__count=1)

    for transaction in transactions:
        process(transaction)
