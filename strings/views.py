from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StringFile
from .serializers import StringFileSerializer
import re


# -------------------- CREATE --------------------
class StringCreateView(generics.CreateAPIView):
    serializer_class = StringFileSerializer
    queryset = StringFile.objects.all()

    def create(self, request, *args, **kwargs):
        value = request.data.get('value')

        # Missing field
        if not value:
            return Response({"error": "Missing 'value' field"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Invalid data type
        if not isinstance(value, str):
            return Response({"error": "Invalid data type for 'value' (must be string)"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Duplicate string
        if StringFile.objects.filter(value=value).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data={'value': value})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------- RETRIEVE --------------------
class StringRetrieveView(generics.RetrieveAPIView):
    serializer_class = StringFileSerializer
    lookup_field = 'value'
    queryset = StringFile.objects.all()


# -------------------- LIST + FILTERS --------------------
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
            qs = qs.filter(value__icontains=filters['contains_character'])

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        filters_applied = {key: request.query_params[key] for key in request.query_params}
        return Response({
            "data": serializer.data,
            "count": queryset.count(),
            "filters_applied": filters_applied
        }, status=status.HTTP_200_OK)


# -------------------- DELETE --------------------
class StringDeleteView(APIView):
    def delete(self, request, string_value):
        instance = StringFile.objects.filter(value=string_value).first()
        if not instance:
            return Response({"error": "String does not exist"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- NATURAL LANGUAGE FILTER --------------------
class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get("query", "").lower()
        if not query:
            return Response({"error": "Missing query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        filters = {}

        # Basic natural language parsing
        if "palindromic" in query or "palindrome" in query:
            filters["is_palindrome"] = True

        if "single word" in query or "one word" in query:
            filters["word_count"] = 1
        elif match := re.search(r"(\d+)\s+word", query):
            filters["word_count"] = int(match.group(1))

        if match := re.search(r"longer than (\d+)", query):
            filters["min_length"] = int(match.group(1)) + 1
        elif match := re.search(r"shorter than (\d+)", query):
            filters["max_length"] = int(match.group(1)) - 1

        if match := re.search(r"letter (\w)", query):
            filters["contains_character"] = match.group(1)
        elif match := re.search(r"contain.*?(\w)", query):
            filters["contains_character"] = match.group(1)

        if not filters:
            return Response({"error": "Unable to parse natural language query"}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({
            "data": serializer.data,
            "count": qs.count(),
            "interpreted_query": {
                "original": query,
                "parsed_filters": filters,
            },
        }, status=status.HTTP_200_OK)
