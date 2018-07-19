from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from ...models import PageRead

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Deletes older PageRead rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "keep_delta", nargs="?", default=settings.KEEP_PAGEREAD_FOR_DAYS, type=int
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Print progress on command line",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]

        keep_delta = options["keep_delta"]

        delete_before = timezone.now() - timedelta(days=keep_delta)

        pageread__count = PageRead.objects.filter(created__lt=delete_before).count()

        if verbose:
            print(
                f"{pageread_count} PageRead entries to delete (older than {delete_before} days)"
            )

        PageRead.objects.filter(created__lt=delete_before).delete()

        logger.info(f"{pageread__count} older PageRead rows deleted")
