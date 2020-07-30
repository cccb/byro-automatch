"""Management command for processing all"""

from django.core.management.base import BaseCommand

from byro_automatch.automatch import transaction


class Command(BaseCommand):
    help = "Run automatch on all potential transactions"

    def handle(self, *args, **options):
        """Run automatch"""
        transaction.process_all()
