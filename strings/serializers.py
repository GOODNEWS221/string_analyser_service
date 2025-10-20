from rest_framework import serializers
from .models import StringFile
from .utils import string_analysis

class StringFileSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    id = serializers.CharField(read_only=True) 

    class Meta:
        model = StringFile
        fields = ['id', 'value', 'properties', 'created_at']

    def get_properties(self, obj):
        return {
            "length": obj.length,
            "is_palindrome": obj.is_palindrome,
            "unique_characters": obj.unique_characters,
            "word_count": obj.word_count,
            "sha256_hash": obj.sha256_hash,
            "character_frequency_map": obj.character_frequency_map,
        }

    def create(self, validated_data):
        value = validated_data['value']
        props = string_analysis(value)
        return StringFile.objects.create(id=props["sha256_hash"], value=value, **props)
