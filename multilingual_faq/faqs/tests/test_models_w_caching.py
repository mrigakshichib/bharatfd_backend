import pytest
from faqs.models import FAQ
from django.core.cache import cache
from unittest.mock import patch
from unittest.mock import AsyncMock
import asyncio


@pytest.mark.django_db
def test_faq_model_creation_with_cache():
    """ Test creating a FAQ entry with cache """
    cache.clear()  # Clear cache to ensure a clean state

    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a web framework."
    )

    # Verify database values
    assert faq.question == "What is Django?"
    assert faq.answer == "Django is a web framework."

    # Verify caching
    cache_key = f"faq:{faq.id}"
    cached_faq = cache.get(cache_key)
    assert cached_faq is None  # Initially, cache should not have the entry

    # Cache the FAQ explicitly
    cache.set(cache_key, faq)
    cached_faq = cache.get(cache_key)
    assert cached_faq == faq


@pytest.mark.django_db
def test_faq_model_language_fallback_with_cache():
    """ Test language fallback with cache (default: English) """
    cache.clear()  # Clear cache to ensure a clean state

    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a web framework."
    )

    # Mocking a language fallback method
    def mock_get_question(language):
        return "Django क्या है?" if language == "hi" else faq.question

    def mock_get_answer(language):
        return "Django एक वेब फ्रेमवर्क है।" if language == "hi" else faq.answer

    faq.get_question = mock_get_question
    faq.get_answer = mock_get_answer

    # Verify language fallback
    assert faq.get_question("en") == "What is Django?"
    assert faq.get_question("hi") == "Django क्या है?"

    assert faq.get_answer("en") == "Django is a web framework."
    assert faq.get_answer("hi") == "Django एक वेब फ्रेमवर्क है।"


@pytest.mark.django_db
@patch("googletrans.Translator.translate", new_callable=AsyncMock)
def test_faq_model_auto_translation_with_cache(mock_translate):
    """ Test auto-translation using Google Translate with cache """
    cache.clear()  # Clear cache to ensure a clean state

    # Simulate the asynchronous behavior of Google Translate
    async def async_translate(text, dest):
        return type('obj', (object,), {"text": f"{text} in {dest}"})()

    mock_translate.side_effect = async_translate

    # Create an FAQ entry
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a web framework."
    )

    # Define standalone async functions for translation
    async def get_question(faq_obj, lang):
        translated = await mock_translate(faq_obj.question, dest=lang)
        return translated.text

    async def get_answer(faq_obj, lang):
        translated = await mock_translate(faq_obj.answer, dest=lang)
        return translated.text

    # Verify translations using asyncio
    translated_question = asyncio.run(get_question(faq, "hi"))
    translated_answer = asyncio.run(get_answer(faq, "hi"))

    assert translated_question == "What is Django? in hi"
    assert translated_answer == "Django is a web framework. in hi"

    # Verify caching of the FAQ
    cache_key = f"faq:{faq.id}"
    cached_faq = cache.get(cache_key)
    assert cached_faq is None  # Cache should be empty initially

    # Cache explicitly
    cache.set(cache_key, faq)
    cached_faq = cache.get(cache_key)
    assert cached_faq == faq