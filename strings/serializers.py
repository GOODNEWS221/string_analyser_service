from rest_framework import serializers
from .models import StringFile

class StringFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringFile
        fields = [
            "id",
            "value",
            "length",
            "is_palindrome",
            "unique_characters",
            "word_count",
            "sha256_hash",
            "character_frequency_map",
            "created_at"
        ]
        read_only_fields = ["id", "length", "is_palindrome", "unique_characters", 
                            "word_count", "sha256_hash", "character_frequency_map", "created_at"]

    # Wrap properties in a `properties` key to match Thanos format
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        properties_keys = ["length", "is_palindrome", "unique_characters", 
                           "word_count", "sha256_hash", "character_frequency_map"]
        rep["properties"] = {k: rep.pop(k) for k in properties_keys}
        return rep
