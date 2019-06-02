from django.db import models
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

import markdown

MARKDOWN_EXTENSIONS = ["extra", "tables", "toc"]


class Tag(models.Model):
    label = models.CharField(max_length=25)
    colour = models.CharField(max_length=7)

    class Meta:
        ordering = ["label"]

    def __str__(self):
        return self.label

    @property
    def dark_colour(self):
        red = int(self.colour[1:3], 16)
        blue = int(self.colour[3:5], 16)
        green = int(self.colour[5:7], 16)
        return (red + blue + green) < 420


class Page(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(verbose_name="Time Created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)
    content = models.TextField(verbose_name="Page content", blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def content_as_html(self):
        return mark_safe(
            markdown.markdown(
                force_text(self.content), MARKDOWN_EXTENSIONS, safe_mode=False
            )
        )

    @property
    def list_tags(self):
        return ", ".join([tag.label for tag in self.tags.all()])

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("page-detail", kwargs={"slug": self.slug})


class PageRead(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.page} {self.created}"
