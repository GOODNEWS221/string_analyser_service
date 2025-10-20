from django.urls import path
from .views import (
    StringCreateView,
    StringRetrieveView,
    StringListView,
    StringDeleteView,
    NaturalLanguageFilterView,
)

urlpatterns = [
    path('strings/', StringListView.as_view(), name='list_strings'),
    path('strings/create/', StringCreateView.as_view(), name='create_string'),
    path('strings/<str:value>/', StringRetrieveView.as_view(), name='get_string'),
    path('strings/<str:value>/delete/', StringDeleteView.as_view(), name='delete_string'),
    path('strings/nlp/', NaturalLanguageFilterView.as_view(), name='nlp_analysis'),
]
