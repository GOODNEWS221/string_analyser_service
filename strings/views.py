from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StringFile
from .serializers import StringFileSerializer
from .utils import string_analysis, parse_natural_language_query


class StringListCreateView(APIView):
    def get(self, request):
        queryset = StringFile.objects.all()

        # HNG-compatible filters
        length = request.query_params.get('length')
        is_palindrome = request.query_params.get('is_palindrome')
        word_count = request.query_params.get('word_count')
        contains_character = request.query_params.get('contains_character')

        if length:
            queryset = queryset.filter(length=int(length))

        if is_palindrome:
            queryset = queryset.filter(is_palindrome=is_palindrome.lower() == 'true')

        if word_count:
            queryset = queryset.filter(word_count=int(word_count))

        if contains_character:
            queryset = queryset.filter(value__icontains=contains_character)

        serializer = StringFileSerializer(queryset, many=True)
        return Response({
            "data": serializer.data,
            "count": queryset.count(),
            "filters_applied": request.query_params
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'value' not in data:
            return Response({"error": "Missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)

        value = data['value']

        if not isinstance(value, str):
            return Response({"error": "'value' must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if StringFile.objects.filter(value=value).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        props = string_analysis(value)
        string_obj = StringFile.objects.create(
            id=props['sha256_hash'],
            value=value,
            length=props['length'],
            is_palindrome=props['is_palindrome'],
            unique_characters=props['unique_characters'],
            word_count=props['word_count'],
            sha256_hash=props['sha256_hash'],
            character_frequency_map=props['character_frequency_map']
        )
        serializer = StringFileSerializer(string_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StringRetrieveView(APIView):
    def get(self, request, value):
        try:
            string_obj = StringFile.objects.get(value=value)
        except StringFile.DoesNotExist:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StringFileSerializer(string_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StringDeleteView(APIView):
    def delete(self, request, value):
        try:
            string_obj = StringFile.objects.get(value=value)
        except StringFile.DoesNotExist:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)

        string_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parsed = parse_natural_language_query(query)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        filters = parsed['parsed_filters']
        queryset = StringFile.objects.all()

        if 'is_palindrome' in filters:
            queryset = queryset.filter(is_palindrome=filters['is_palindrome'])
        if 'word_count' in filters:
            queryset = queryset.filter(word_count=filters['word_count'])
        if 'min_length' in filters:
            queryset = queryset.filter(length__gte=filters['min_length'])
        if 'max_length' in filters:
            queryset = queryset.filter(length__lte=filters['max_length'])
        if 'contains_character' in filters:
            queryset = queryset.filter(value__icontains=filters['contains_character'])

        serializer = StringFileSerializer(queryset, many=True)
        return Response({
            "data": serializer.data,
            "count": queryset.count(),
            "filters_applied": filters  # <-- HNG expects this key
        }, status=status.HTTP_200_OK)



