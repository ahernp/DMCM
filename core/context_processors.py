from collections import OrderedDict

from django.conf import settings
from django.db.models import Count

from mpages.models import Page, PageRead

NUMBER_OF_PAGES_IN_HISTORY = 20


def menus(request):
    main_menu = Page.objects.get(slug="main-menu")

    page_reads = PageRead.objects.all()
    history = []
    for page_read in page_reads:
        if page_read.page not in history:
            history.append(page_read.page)
        if len(history) == NUMBER_OF_PAGES_IN_HISTORY-1:
            break

    return {
        "mainmenu": main_menu.content_as_html,
        "sidebar": {
            "history": history,
        },
        "request": request,
    }
