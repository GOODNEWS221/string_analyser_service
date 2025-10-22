from rest_framework import serializers
from .models import AnalyzedString
from .utils import analyze_string
import hashlib

class AnalyzedStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedString
        fields = "__all__"
        read_only_fields = ("sha256_hash", "length", "is_palindrome", "unique_characters", "word_count", "character_frequency_map", "created_at")

    value = serializers.CharField()

    def create(self, validated_data):
        value = validated_data.get("value")
        analysis = analyze_string(value)
        validated_data.update(analysis)
        validated_data["sha256_hash"] = hashlib.sha256(value.encode("utf-8")).hexdigest()
        return super().create(validated_data)
