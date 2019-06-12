from django.core.management.base import BaseCommand

from ...models import Page

import logging

logger = logging.getLogger(__name__)

OUTPUT_DIRECTORY = "data"


class Command(BaseCommand):
    help = "Extract Pages as individual Markdown files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Print progress on command line",
        )

    def handle(self, *args, **options):
        verbose = options["verbose"]

        pages = Page.objects.all()
        number_of_pages = len(pages)

        for count, page in enumerate(pages, start=1):
            f = open(f"{OUTPUT_DIRECTORY}/{page.slug}.md", "w")
            f.write(page.content)
            f.close()

            if verbose:
                print(
                    f"{count}/{number_of_pages} Page {page.title} written"
            )
