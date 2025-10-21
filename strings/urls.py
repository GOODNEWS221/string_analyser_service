from django.urls import path
from .views import (
    StringListCreateView,
    StringRetrieveView,
    StringDeleteView,
    NaturalLanguageFilterView,
)

urlpatterns = [
    # Handles both GET and POST
    path('strings/', StringListCreateView.as_view(), name='list_create_strings'),

    # Retrieve specific string
    path('strings/<str:value>/', StringRetrieveView.as_view(), name='get_string'),

    # Delete specific string
    path('strings/<str:value>/', StringDeleteView.as_view(), name='delete_string'),

    # Natural language filter
    path('strings/filter-by-natural-language/', NaturalLanguageFilterView.as_view(), name='nlp_analysis'),
]
