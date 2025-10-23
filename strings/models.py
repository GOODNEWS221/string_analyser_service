from django.db import models
import hashlib

class AnalyzedString(models.Model):
    value = models.CharField(max_length=500, unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Compute SHA256 hash
        self.sha256_hash = hashlib.sha256(self.value.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
