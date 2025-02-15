from rest_framework import serializers
from .models import Word, Group

class GroupSerializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'word_count']

    def get_word_count(self, obj):
        return obj.words.count()

class WordSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = ['japanese', 'romaji', 'english', 'stats', 'groups']

    def get_stats(self, obj):
        try:
            return obj.stats
        except AttributeError:
            return {
                "correct_count": 0,
                "wrong_count": 0
            } 