from collections import OrderedDict

from django.conf import settings
from django.db.models import Count

from mpages.models import Page, PageRead


def menus(request):
    main_menu = Page.objects.get(slug="main-menu")

    recent_updates = Page.objects.all().order_by("-updated")[:5]
    updates = OrderedDict()
    for page in recent_updates:
        update_date = page.updated.strftime("%Y-%m-%d")
        if update_date not in updates:
            updates[update_date] = {"date": update_date, "pages": []}
        updates[update_date]["pages"].append(page)

    page_reads = PageRead.objects.all()[:50]
    recent = []
    for page_read in page_reads:
        if page_read.page not in recent:
            recent.append(page_read.page)
        if len(recent) == 6:
            break

    popular = (
        PageRead.objects.exclude(page__slug=settings.HOMEPAGE_SLUG)
        .exclude(page__slug=settings.TASK_LIST_SLUG)
        .values("page__slug", "page__title")
        .annotate(total=Count("page__slug"))
        .order_by("-total", "page__slug")[:5]
    )

    return {
        "mainmenu": main_menu.content_as_html,
        "sidebar": {
            "updates": list(updates.values()),
            "recent": recent[1:],
            "popular": popular,
        },
        "request": request,
    }
