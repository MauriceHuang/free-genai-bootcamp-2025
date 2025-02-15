from rest_framework import serializers
from study.models import StudySession
from words.models import Word

class LastStudySessionSerializer(serializers.ModelSerializer):
    """
    Serializer for the most recent study session.
    
    Purpose:
    - Provides information about the user's last study activity
    - Used in the dashboard to show the most recent learning progress
    - Includes activity name, group name, and timing information
    
    Example Response:
    {
        "id": 1,
        "activity_name": "Typing Exercise",
        "group_name": "Basic Greetings",
        "created_at": "2025-02-08T22:20:23Z",
        "end_time": "2025-02-08T22:30:23Z",
        "review_items_count": 3
    }
    """
    activity_name = serializers.CharField(source='study_activity.name')
    group_name = serializers.CharField(source='group.name')
    
    class Meta:
        model = StudySession
        fields = [
            'id',
            'activity_name',
            'group_name',
            'created_at',
            'end_time',
            'review_items_count'
        ]

class StudyProgressSerializer(serializers.Serializer):
    """
    Serializer for overall study progress statistics.
    
    Purpose:
    - Shows the user's overall learning progress
    - Tracks how many unique words have been studied
    - Helps users understand their coverage of available vocabulary
    
    Example Response:
    {
        "total_words_studied": 25,
        "total_available_words": 100
    }
    """
    total_words_studied = serializers.IntegerField()
    total_available_words = serializers.IntegerField()

class QuickStatsSerializer(serializers.Serializer):
    """
    Serializer for quick overview statistics.
    
    Purpose:
    - Provides key performance indicators (KPIs) for the dashboard
    - Shows success rate to track learning effectiveness
    - Monitors engagement through session and group counts
    - Tracks learning consistency with study streak
    
    Example Response:
    {
        "success_rate": 80.5,
        "total_study_sessions": 42,
        "total_active_groups": 3,
        "study_streak_days": 5
    }
    """
    success_rate = serializers.FloatField()
    total_study_sessions = serializers.IntegerField()
    total_active_groups = serializers.IntegerField()
    study_streak_days = serializers.IntegerField() 