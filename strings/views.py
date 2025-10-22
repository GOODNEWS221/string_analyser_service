from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import parse_natural_language

class StringListCreateAPIView(APIView):
    def post(self, request):
        if "value" not in request.data:
            return Response({"error": "Missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(request.data["value"], str):
            return Response({"error": "'value' must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if AnalyzedString.objects.filter(value=request.data["value"]).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        serializer = AnalyzedStringSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        qs = AnalyzedString.objects.all()
        filters_applied = {}

        # Filters from query params
        is_palindrome = request.query_params.get("is_palindrome")
        if is_palindrome is not None:
            qs = qs.filter(is_palindrome=is_palindrome.lower() == "true")
            filters_applied["is_palindrome"] = is_palindrome
        min_length = request.query_params.get("min_length")
        if min_length:
            qs = qs.filter(length__gte=int(min_length))
            filters_applied["min_length"] = min_length
        max_length = request.query_params.get("max_length")
        if max_length:
            qs = qs.filter(length__lte=int(max_length))
            filters_applied["max_length"] = max_length
        word_count = request.query_params.get("word_count")
        if word_count:
            qs = qs.filter(word_count=int(word_count))
            filters_applied["word_count"] = word_count
        contains_character = request.query_params.get("contains_character")
        if contains_character:
            qs = [s for s in qs if contains_character in s.value]
            filters_applied["contains_character"] = contains_character

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data), "filters_applied": filters_applied})

class StringRetrieveDeleteAPIView(APIView):
    def get(self, request, string_value):
        try:
            s = AnalyzedString.objects.get(value=string_value)
            serializer = AnalyzedStringSerializer(s)
            return Response(serializer.data)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, string_value):
        try:
            s = AnalyzedString.objects.get(value=string_value)
            s.delete()
            return Response({"message": f"String '{string_value}' deleted"}, status=status.HTTP_200_OK)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)

class StringNaturalLanguageFilterAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "Missing query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        filters = parse_natural_language(query)
        qs = AnalyzedString.objects.all()
        if filters.get("is_palindrome") is not None:
            qs = qs.filter(is_palindrome=filters["is_palindrome"])
        if filters.get("word_count") is not None:
            qs = qs.filter(word_count=filters["word_count"])
        if filters.get("length") is not None:
            qs = qs.filter(length=filters["length"])
        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response({"data": serializer.data, "count": len(serializer.data), "interpreted_query": {"original": query, "parsed_filters": filters}})
