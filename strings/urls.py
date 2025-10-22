from django.urls import path
from .views import (
    StringListCreateView,
    StringRetrieveDeleteView,   # Combined GET & DELETE
    NaturalLanguageFilterView
)

urlpatterns = [
    # Create / List strings
    path('strings/', StringListCreateView.as_view(), name='list_create_strings'),

    # Retrieve single string or delete it
    path('strings/<str:value>/', StringRetrieveDeleteView.as_view(), name='get_delete_string'),

    # Natural language filtering
    path('strings/filter-by-natural-language/', NaturalLanguageFilterView.as_view(), name='nlp_analysis'),
]
