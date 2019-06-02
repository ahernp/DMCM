from django.contrib import admin

from .models import Page, PageRead, Tag


class PageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "parent", "updated"]
    list_filter = ["tags"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["updated"]
    ordering = ["parent", "title"]
    filter_horizontal = ("tags",)
    save_on_top = True
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("content",),
                    ("title", "parent"),
                    ("slug", "updated"),
                    ("tags",),
                )
            },
        ),
    )
    autocomplete_fields = ["parent"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Page.objects.order_by("title")
        return super(PageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class PageReadAdmin(admin.ModelAdmin):
    search_fields = ["page__title"]


admin.site.register(Page, PageAdmin)
admin.site.register(PageRead, PageReadAdmin)
admin.site.register(Tag)
