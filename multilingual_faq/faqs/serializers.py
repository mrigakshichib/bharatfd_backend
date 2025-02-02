from rest_framework import serializers
from .models import FAQ
from django.core.cache import cache
from deep_translator import GoogleTranslator

class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQ with caching for translations """

    question = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        """
          Dynamically handle language-based filtering only for GET requests.
        """
        super().__init__(*args, **kwargs)

        # Apply translation only for GET requests
        if self.context.get("request") and self.context["request"].method == "GET":
            lang = self.context.get('lang', 'en')

            if lang in ["hi", "bn"]:
                self.fields["question"] = serializers.SerializerMethodField()
                self.fields["answer"] = serializers.SerializerMethodField()

    def get_question(self, obj):
        """   Fetch translated question from cache or translate if needed """
        lang = self.context.get('lang', 'en')
        return self._get_cached_translation(obj.question, lang)

    def get_answer(self, obj):
        """   Fetch translated answer from cache or translate if needed """
        lang = self.context.get('lang', 'en')
        return self._get_cached_translation(obj.answer, lang)

    def _get_cached_translation(self, text, lang):
        """   Helper function to cache translations """
        if lang == "en":
            return text  # No translation needed

        cache_key = f"translation_{lang}_{text}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            return cached_translation

        translated_text = GoogleTranslator(source='en', target=lang).translate(text)
        cache.set(cache_key, translated_text, timeout=24 * 60 * 60)  # Cache for 24 hours
        return translated_text
