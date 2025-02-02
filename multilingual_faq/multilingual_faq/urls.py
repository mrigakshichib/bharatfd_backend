from django.contrib import admin
from django.urls import path
from faqs.views import FAQListCreateView, FAQDetailView, translate_text

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('api/faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]
