import pytest
from rest_framework.test import APIClient
from django.core.cache import cache
from faqs.models import FAQ


@pytest.mark.django_db
def test_create_faq():
    """  Test creating an FAQ via API """
    cache.clear()

    client = APIClient()
    payload = {
        "question": "What is Django?",
        "answer": "Django is a Python web framework.",
    }

    response = client.post("/api/faqs/", payload)
    
    assert response.status_code == 201
    assert response.data["question"] == "What is Django?"
    assert response.data["answer"] == "Django is a Python web framework."

    # Verify FAQ is created in DB
    faq = FAQ.objects.first()
    assert faq is not None
    assert faq.question == "What is Django?"
    assert faq.answer == "Django is a Python web framework."


@pytest.mark.django_db
def test_get_faq_list():
    """  Test retrieving FAQ list via API """
    cache.clear()
    
    FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python web framework."
    )

    client = APIClient()
    response = client.get("/api/faqs/")
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["question"] == "What is Django?"
    assert response.data[0]["answer"] == "Django is a Python web framework."


@pytest.mark.django_db
def test_get_faq_in_hindi_with_cache():
    """  Test retrieving FAQ in Hindi with caching """
    cache.clear()

    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python web framework."
    )

    #  Manually cache translations
    cache.set(f"faq_system:translation:hi:{faq.question}", "Django क्या है?", timeout=24 * 60 * 60)
    cache.set(f"faq_system:translation:hi:{faq.answer}", "Django एक पायथन वेब फ्रेमवर्क है।", timeout=24 * 60 * 60)

    client = APIClient()
    response = client.get("/api/faqs/?lang=hi")

    assert response.status_code == 200
    assert response.data[0]["question"] == "Django क्या है?"
    assert response.data[0]["answer"] == "Django एक पायथन वेब फ्रेमवर्क है।"
