from collections import OrderedDict

from mpages.models import Page


def menus(request):
    main_menu = Page.objects.get(slug="main-menu")
    recent_updates = Page.objects.all().order_by("-updated")[:10]
    updates = OrderedDict()
    for page in recent_updates:
        update_date = page.updated.strftime("%Y-%m-%d")
        if update_date not in updates:
            updates[update_date] = {"date": update_date, "pages": []}
        updates[update_date]["pages"].append(page)
    return {
        "mainmenu": main_menu.content_as_html,
        "sidebar": {"updates": list(updates.values())},
        "request": request,
    }
