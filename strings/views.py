from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StringFile
from .serializers import StringFileSerializer
from .utils import string_analysis, parse_natural_language_query


class StringListCreateView(APIView):
    def get(self, request):
        queryset = StringFile.objects.all()
        filters = {}

        # Apply query filters
        if 'is_palindrome' in request.query_params:
            filters['is_palindrome'] = request.query_params.get('is_palindrome').lower() == 'true'
        if 'min_length' in request.query_params:
            queryset = queryset.filter(length__gte=int(request.query_params['min_length']))
        if 'max_length' in request.query_params:
            queryset = queryset.filter(length__lte=int(request.query_params['max_length']))
        if 'word_count' in request.query_params:
            queryset = queryset.filter(word_count=int(request.query_params['word_count']))
        if 'contains_character' in request.query_params:
            char = request.query_params['contains_character']
            queryset = queryset.filter(value__icontains=char)

        serializer = StringFileSerializer(queryset, many=True)
        return Response({
            "data": serializer.data,
            "count": queryset.count(),
            "filters_applied": request.query_params
        })

    def post(self, request):
        data = request.data

        # Missing 'value' field
        if 'value' not in data:
            return Response({"error": "Missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)

        value = data['value']

        # Invalid data type
        if not isinstance(value, str):
            return Response({"error": "'value' must be a string"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Duplicate string
        if StringFile.objects.filter(value=value).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        props = string_analysis(value)
        string_obj = StringFile.objects.create(id=props['sha256_hash'], value=value, **props)
        serializer = StringFileSerializer(string_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StringRetrieveView(APIView):
    def get(self, request, value):
        try:
            string_obj = StringFile.objects.get(value=value)
        except StringFile.DoesNotExist:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StringFileSerializer(string_obj)
        return Response(serializer.data)


class StringDeleteView(APIView):
    def delete(self, request, value):
        try:
            string_obj = StringFile.objects.get(value=value)
        except StringFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
            "interpreted_query": parsed
        })
