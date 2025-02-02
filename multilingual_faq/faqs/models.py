from django.db import models
from ckeditor.fields import RichTextField
from deep_translator import GoogleTranslator
from django.core.cache import cache

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FAQ #{self.pk}"

    def save(self, *args, **kwargs):
        """ Save the FAQ and cache its translations. """
        super().save(*args, **kwargs)
        self._cache_translations()

    def _cache_translations(self):
        """ Caches translations for this FAQ in Redis. """
        # Generate a unique cache key for each FAQ using its question text
        cache_key = f"faq_system:translation:{self.pk}"  # Unique identifier for the FAQ translations
        cached_data = cache.get(cache_key)

        if not cached_data:
            print(f"⏳ Caching translations for {cache_key}")

            # Store translations for all supported languages in the cache
            cached_data = {
                "question_hi": self._translate_text(self.question, "hi"),
                "answer_hi": self._translate_text(self.answer, "hi"),
                "question_bn": self._translate_text(self.question, "bn"),
                "answer_bn": self._translate_text(self.answer, "bn"),
            }
            
            # Cache the translations dictionary for 24 hours
            cache.set(cache_key, cached_data, timeout=24 * 60 * 60)
        else:
            print(f" Translation cache HIT: {cache_key}")

    def _translate_text(self, text, target_lang):
        """ Helper function to translate text & store in cache. """
        if not text:
            return ""

        # Define the Redis key explicitly
        cache_key = f"faq_system:translation:{target_lang}:{text}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            print(f"  Translation cache HIT: {cache_key}")
            return cached_translation

        print(f"⏳ Translating and caching: {cache_key}")
        translated_text = GoogleTranslator(source='en', target=target_lang).translate(text)
        cache.set(cache_key, translated_text, timeout=24 * 60 * 60)
        return translated_text
    

    def get_question(self, lang='en'):
        """ Returns translated question from cache or original question """
        if lang == 'hi':
            cached_translation = cache.get(f"faq_system:translation:hi:{self.question}")
            return cached_translation if cached_translation else self.question
        if lang == 'bn':
            cached_translation = cache.get(f"faq_system:translation:bn:{self.question}")
            return cached_translation if cached_translation else self.question
        return self.question  # Default to English

    def get_answer(self, lang='en'):
        """ Returns translated answer from cache or original answer """
        if lang == 'hi':
            cached_translation = cache.get(f"faq_system:translation:hi:{self.answer}")
            return cached_translation if cached_translation else self.answer
        if lang == 'bn':
            cached_translation = cache.get(f"faq_system:translation:bn:{self.answer}")
            return cached_translation if cached_translation else self.answer
        return self.answer  # Default to English