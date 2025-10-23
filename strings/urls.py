from django.urls import path
from .views import (
    StringListCreateAPIView,
    StringRetrieveDeleteAPIView,   # Combined GET & DELETE
    StringNaturalLanguageFilterAPIView
)

urlpatterns = [
    # Create / List strings
    path('strings/', StringListCreateAPIView.as_view(), name='list_create_strings'),

    # Retrieve single string or delete it
    path('strings/<str:value>/', StringRetrieveDeleteAPIView.as_view(), name='get_delete_string'),

    # Natural language filtering
    path('strings/filter-by-natural-language/', StringNaturalLanguageFilterAPIView.as_view(), name='nlp_analysis'),
]
