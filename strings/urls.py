from django.urls import path
from .views import (
    StringListCreateView,
    StringRetrieveView,
    StringDeleteView,
    NaturalLanguageFilterView,
)

urlpatterns = [
    path('strings', StringListCreateView.as_view(), name='list_create_strings'),
    path('strings/<str:value>', StringRetrieveView.as_view(), name='get_string'),
    path('strings/<str:value>/delete', StringDeleteView.as_view(), name='delete_string'),
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='nlp_analysis'),
]
