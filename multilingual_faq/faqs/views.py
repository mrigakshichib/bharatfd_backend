from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from deep_translator import GoogleTranslator


def translate_text(request):
    """
      Translate text from one language to another using the Google Translate API with caching.
    """
    if request.method == 'POST':
        data = request.POST
        text = data.get('text')
        source_language = data.get('source_language', 'auto')  # Detect language if not provided
        target_language = data.get('target_language')

        if not text or not target_language:
            return JsonResponse({'error': 'Text and target_language are required.'}, status=400)

        # Normalize the cache key to remove unwanted prefixes
        cache_key = f"faq_system:translation:{source_language}:{target_language}:{text}"
        cached_translation = cache.get(cache_key)

        if cached_translation:
            return JsonResponse({'translated_text': cached_translation}, status=200)

        try:
            # Translate and store in cache
            translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
            cache.set(cache_key, translated, timeout=24 * 60 * 60)  # Cache for 24 hours
            return JsonResponse({'translated_text': translated}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=400)

class FAQListCreateView(generics.ListCreateAPIView):
    """   Handles listing all FAQs and creating a new FAQ with caching. """
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_serializer_context(self):
        """   Pass `lang` from request query parameters to the serializer """
        context = super().get_serializer_context()
        context["lang"] = self.request.query_params.get("lang", "en")
        context["request"] = self.request  #   Add request context
        return context

    def create(self, request, *args, **kwargs):
        """   Ensure fields are properly saved on POST requests. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()  #   Save the instance

        # Return full response with stored values
        response_data = FAQSerializer(instance, context={"request": request}).data
        return Response(response_data, status=status.HTTP_201_CREATED)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting an FAQ by ID."""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
