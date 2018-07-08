from mpages.models import Page


def menus(request):
    main_menu = Page.objects.get(slug="main-menu")
    return {
        "mainmenu": main_menu.content_as_html,
        "sidebar": "Sidebar",
        "request": request,
    }
