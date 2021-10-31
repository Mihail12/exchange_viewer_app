from django.urls import path

from quotes.views import QuotesAPIView

urlpatterns = [
    path('api/v1/quotes/', QuotesAPIView.as_view(), name='quotes'),
]
