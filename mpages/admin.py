from django.contrib import admin

from .models import Page, PageRead, Tag


class PageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "parent", "updated"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["updated"]
    ordering = ["parent", "title"]
    filter_horizontal = ('tags',)
    save_on_top = True
    fieldsets = (
        (None, {"fields": (("content",), ("title", "parent"), ("slug", "updated"), ("tags",))}),
    )


admin.site.register(Page, PageAdmin)
admin.site.register(PageRead)
admin.site.register(Tag)
