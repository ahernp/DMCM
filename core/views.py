from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.conf import settings
from django.db.models import F
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import UploadForm, FILE_TYPE_CHOICES
from .utils import Headline, highlight_matching_substring, run_shell_command
from mpages.models import Page


def list_uploads():
    cwd = settings.BASE_DIR
    uploads = []
    for upload_type in FILE_TYPE_CHOICES:
        for filename in run_shell_command(
            f"ls media/{upload_type.directory}/*.*", cwd
        ).split():
            uploads.append(
                {
                    "type": upload_type.label,
                    "directory": upload_type.directory,
                    "filename": filename.split("/")[2],
                }
            )
    return uploads


class SearchView(TemplateView):
    template_name = "core/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_string = self.request.GET.get("search", "")
        results = OrderedDict()
        if len(search_string) >= 3:
            search_query = SearchQuery(search_string)
            title_vector = SearchVector("title", weight="A")

            content_vector = SearchVector("content", weight="B")
            page_vectors = title_vector + content_vector

            pages = (
                Page.objects.annotate(search=page_vectors)
                .filter(search=search_query)
                .annotate(rank=SearchRank(page_vectors, search_query))
                .order_by("-rank")
                .annotate(title_highlight=Headline(F("title"), search_query))
                .annotate(content_highlight=Headline(F("content"), search_query))
            )

            for page in pages:
                results[page.slug] = {
                    "slug": page.slug,
                    "title_highlight": page.title_highlight,
                    "content_highlight": page.content_highlight,
                }

            pages = Page.objects.filter(title__icontains=search_string)
            for page in pages:
                if page.slug not in results:
                    results[page.slug] = {
                        "slug": page.slug,
                        "title_highlight": highlight_matching_substring(
                            page.title, search_string
                        ),
                        "content_highlight": highlight_matching_substring(
                            page.content, search_string
                        ),
                    }

            pages = Page.objects.filter(content__icontains=search_string)
            for page in pages:
                if page.slug not in results:
                    results[page.slug] = {
                        "slug": page.slug,
                        "title_highlight": highlight_matching_substring(
                            page.title, search_string
                        ),
                        "content_highlight": highlight_matching_substring(
                            page.content, search_string
                        ),
                    }

            context["results"] = list(results.values())

            uploads = [
                upload
                for upload in list_uploads()
                if search_string.lower() in upload["filename"].lower()
            ]
            for upload in uploads:
                upload["filename_highlight"] = highlight_matching_substring(
                    upload["filename"], search_string
                )
            context["uploads"] = uploads
        else:
            context["error"] = "Search term must be at least 3 characters"
        context["search_string"] = search_string
        return context


class UploadView(LoginRequiredMixin, FormView):
    template_name = "core/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        upload_file = form.cleaned_data["upload_file"]
        upload_file_type = form.cleaned_data["upload_type"]
        with open(
            f"{settings.MEDIA_ROOT}/{upload_file_type}/{upload_file.name}", "wb+"
        ) as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["uploads"] = list_uploads()

        return context

    def get_success_url(self):
        return reverse("upload")
