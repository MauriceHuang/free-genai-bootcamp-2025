from rest_framework import serializers
from .models import StudyActivity, StudySession, WordReviewItem
from words.serializers import WordSerializer, GroupSerializer

class StudyActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for study activities (e.g., Typing Exercise, Flashcards)
    """
    class Meta:
        model = StudyActivity
        fields = ['id', 'name', 'thumbnail_url', 'description']

class WordReviewItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual word reviews within a study session
    """
    word = WordSerializer(read_only=True)

    class Meta:
        model = WordReviewItem
        fields = ['word', 'correct', 'created_at']

class StudySessionSerializer(serializers.ModelSerializer):
    """
    Serializer for study sessions with related data
    """
    activity_name = serializers.CharField(source='study_activity.name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    review_items_count = serializers.IntegerField(read_only=True)
    start_time = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = StudySession
        fields = [
            'id',
            'activity_name',
            'group_name',
            'start_time',
            'end_time',
            'review_items_count'
        ]

class StudySessionDetailSerializer(StudySessionSerializer):
    """
    Detailed serializer for study sessions, including review items
    """
    review_items = WordReviewItemSerializer(
        source='wordreviewitem_set',
        many=True,
        read_only=True
    )

    class Meta(StudySessionSerializer.Meta):
        fields = StudySessionSerializer.Meta.fields + ['review_items']

class CreateStudySessionSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new study sessions
    """
    class Meta:
        model = StudySession
        fields = ['group', 'study_activity']

    def create(self, validated_data):
        return StudySession.objects.create(**validated_data)

class WordReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating word reviews
    """
    class Meta:
        model = WordReviewItem
        fields = ['word', 'study_session', 'correct']

    def create(self, validated_data):
        return WordReviewItem.objects.create(**validated_data) 