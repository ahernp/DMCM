from collections import OrderedDict

from django.conf import settings
from django.db.models import Count

from mpages.models import Page, PageRead

NUMBER_OF_PAGES_IN_HISTORY = 6


def menus(request):
    main_menu = Page.objects.get(slug="main-menu")

    recent_updates = Page.objects.all().order_by("-updated")[:NUMBER_OF_PAGES_IN_HISTORY-1]
    updates = OrderedDict()
    for page in recent_updates:
        update_date = page.updated.strftime("%Y-%m-%d")
        if update_date not in updates:
            updates[update_date] = {"date": update_date, "pages": []}
        updates[update_date]["pages"].append(page)

    page_reads = PageRead.objects.all()
    recent = []
    for page_read in page_reads:
        if page_read.page not in recent:
            recent.append(page_read.page)
        if len(recent) == NUMBER_OF_PAGES_IN_HISTORY-1:
            break

    popular = (
        PageRead.objects.exclude(page__slug=settings.HOMEPAGE_SLUG)
        .exclude(page__slug=settings.TASK_LIST_SLUG)
        .values("page__slug", "page__title")
        .annotate(total=Count("page__slug"))
        .order_by("-total", "page__slug")[:NUMBER_OF_PAGES_IN_HISTORY-1]
    )

    return {
        "mainmenu": main_menu.content_as_html,
        "sidebar": {
            "updates": list(updates.values()),
            "recent": recent,
            "popular": popular,
        },
        "request": request,
    }
