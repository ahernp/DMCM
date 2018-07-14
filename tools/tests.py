import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_tools_view(client):
    response = client.get(reverse("tools"))
    assert response.status_code == 200
    assert b"<title>Tools</title>" in response.content


@pytest.mark.django_db
def test_tool_view(client):
    response = client.get(reverse("tool", kwargs={"tool": "match"}))
    assert response.status_code == 200
    assert b"<title>Tools</title>" in response.content
