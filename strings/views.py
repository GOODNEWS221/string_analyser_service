from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import StringFile
from .serializers import StringFileSerializer
from .utils import string_analysis
import re

class StringCreateView(generics.CreateAPIView):
    serializer_class = StringFileSerializer
    queryset = StringFile.objects.all()

    def create(self, request, *args, **kwargs):
        value = request.data.get('value')
        if not value:
            return Response({"error": "Missing 'value' field"}, status=400)
        if not isinstance(value, str):
            return Response({"error": "Value must be a string"}, status=422)
        if StringFile.objects.filter(value=value).exists():
            return Response({"error": "String already exists"}, status=409)

        serializer = self.get_serializer(data={'value': value})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data, status=201)


class StringRetrieveView(generics.RetrieveAPIView):
    serializer_class = StringFileSerializer
    lookup_field = 'value'
    queryset = StringFile.objects.all()


class StringListView(generics.ListAPIView):
    serializer_class = StringFileSerializer

    def get_queryset(self):
        qs = StringFile.objects.all()
        filters = self.request.query_params

        if 'is_palindrome' in filters:
            qs = qs.filter(is_palindrome=filters['is_palindrome'].lower() == 'true')
        if 'min_length' in filters:
            qs = qs.filter(length__gte=int(filters['min_length']))
        if 'max_length' in filters:
            qs = qs.filter(length__lte=int(filters['max_length']))
        if 'word_count' in filters:
            qs = qs.filter(word_count=int(filters['word_count']))
        if 'contains_character' in filters:
            char = filters['contains_character']
            qs = qs.filter(value__icontains=char)

        return qs


class StringDeleteView(APIView):
    """
    DELETE /strings/{string_value}
    Deletes a string record if it exists
    """
    def delete(self, request, string_value):
        instance = StringFile.objects.filter(value=string_value).first()
        if not instance:
            return Response({"error": "String does not exist"}, status=404)
        instance.delete()
        return Response(status=204)


class NaturalLanguageFilterView(APIView):
    """
    GET /strings/filter-by-natural-language?query=<query>
    Parses a simple natural language query and filters strings accordingly.
    """

    def get(self, request):
        query = request.query_params.get("query", "").lower()
        if not query:
            return Response({"error": "Missing query parameter"}, status=400)

        filters = {}

        # Simple natural language parsing
        if "palindromic" in query or "palindrome" in query:
            filters["is_palindrome"] = True

        if "single word" in query or "one word" in query:
            filters["word_count"] = 1
        elif match := re.search(r"(\d+)\s+word", query):
            filters["word_count"] = int(match.group(1))

        if match := re.search(r"longer than (\d+)", query):
            filters["min_length"] = int(match.group(1)) + 1

        if match := re.search(r"shorter than (\d+)", query):
            filters["max_length"] = int(match.group(1)) - 1

        if match := re.search(r"letter (\w)", query):
            filters["contains_character"] = match.group(1)
        elif match := re.search(r"contain.*?(\w)", query):
            filters["contains_character"] = match.group(1)

        if not filters:
            return Response(
                {"error": "Unable to parse natural language query"}, status=400
            )

        # Apply filters to queryset
        qs = StringFile.objects.all()
        if "is_palindrome" in filters:
            qs = qs.filter(is_palindrome=True)
        if "min_length" in filters:
            qs = qs.filter(length__gte=filters["min_length"])
        if "max_length" in filters:
            qs = qs.filter(length__lte=filters["max_length"])
        if "word_count" in filters:
            qs = qs.filter(word_count=filters["word_count"])
        if "contains_character" in filters:
            qs = qs.filter(value__icontains=filters["contains_character"])

        serializer = StringFileSerializer(qs, many=True)
        return Response(
            {
                "data": serializer.data,
                "count": qs.count(),
                "interpreted_query": {
                    "original": query,
                    "parsed_filters": filters,
                },
            },
            status=200,
        )


