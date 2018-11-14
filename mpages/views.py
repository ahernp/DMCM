from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect

from .models import Page, PageRead


class PageListView(ListView):
    model = Page
    parent = None

    def get_queryset(self):
        parent_slug = self.kwargs.get("parent_slug", None)
        if parent_slug:
            self.parent = get_object_or_404(Page, slug=parent_slug)
            return Page.objects.filter(parent=self.parent)
        return Page.objects.all().select_related("parent")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list, **kwargs)
        context["parent"] = self.parent
        return context


class PageDetailView(DetailView):
    model = Page

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            slug = kwargs.get("slug", "")
            populate_fields = f"?slug={slug}&title={slug}"
            return redirect(reverse("admin:mpages_page_add") + populate_fields)
        PageRead.objects.create(page=self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PageEditView(LoginRequiredMixin, DetailView):
    model = Page
    template_name = "mpages/page_edit.html"
