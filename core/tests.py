import pytest

import datetime
import unittest

from django.urls import reverse
from django.utils import timezone

from pages.factories import PageFactory
from .factories import LogFactory
from .utils import highlight_matching_substring


@pytest.mark.django_db
def test_search(client):
    page = PageFactory.create()
    response = client.get(f'{reverse("search")}?search=page')
    assert response.status_code == 200
    assert b"<title>Search Results</title>" in response.content
    assert bytes(f'<a href="{page.get_absolute_url()}">', "utf-8") in response.content


@pytest.mark.django_db
def test_upload_page(admin_client):
    response = admin_client.get(reverse("upload"), follow=True)
    assert response.status_code == 200
    assert b"<title>Upload Files</title>" in response.content


def test_recent_logs():
    log = LogFactory.create()
    assert log.recent() == True, "Newly created log is recent"

    log.datetime = timezone.now() - datetime.timedelta(days=2)
    assert log.recent() == False, "Two day old log is not recent"


@pytest.mark.parametrize(
    "string, substring, expected_result",
    [
        ("In the beginning", "wibble", "In the beg..."),
        ("In the\nbeginning", "beg", "<b>beg</b>inning"),
        ("In the beginning", "beg", "<b>beg</b>inning"),
        ("Inthebeginning", "beg", "<b>beg</b>inning"),
        ("Beg leave to report", "beg", "<b>Beg</b> leave ..."),
    ],
)
def test_highlight_matching_substring(string, substring, expected_result):
    result = highlight_matching_substring(string, substring, max_length=10)
    assert result == expected_result
