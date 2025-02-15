from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from typing import Dict, Union, Any

from study.models import StudySession, WordReviewItem
from words.models import Word, Group
from .serializers import (
    LastStudySessionSerializer,
    StudyProgressSerializer,
    QuickStatsSerializer
)

class LastStudySessionView(APIView):
    """
    Retrieve information about the most recent study session.
    
    Returns:
        Response with the last study session data including:
        - id: Session identifier
        - activity_name: Name of the study activity
        - group_name: Name of the word group
        - created_at: Session start time
        - end_time: Session end time
        - review_items_count: Number of words reviewed
        
    If no sessions exist, returns a message indicating no sessions found.
    """
    def get(self, request) -> Response:
        try:
            last_session = StudySession.objects.select_related(
                'study_activity', 'group'
            ).order_by('-created_at').first()
            
            if not last_session:
                return Response(
                    {"message": "No study sessions found"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = LastStudySessionSerializer(last_session)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StudyProgressView(APIView):
    """
    Retrieve overall study progress statistics.
    
    Returns:
        Response with study progress data including:
        - total_words_studied: Number of unique words reviewed
        - total_available_words: Total number of words in the system
        
    The progress can be used to show completion percentage in the UI.
    """
    def get(self, request) -> Response:
        try:
            # Get unique words that have been studied (have review items)
            total_words_studied = Word.objects.filter(
                wordreviewitem__isnull=False
            ).distinct().count()
            
            # Get total available words
            total_available_words = Word.objects.count()
            
            data = {
                'total_words_studied': total_words_studied,
                'total_available_words': total_available_words
            }
            
            serializer = StudyProgressSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuickStatsView(APIView):
    """
    Retrieve quick overview statistics for the dashboard.
    
    Returns:
        Response with statistics including:
        - success_rate: Percentage of correct word reviews
        - total_study_sessions: Number of study sessions
        - total_active_groups: Number of groups with study sessions
        - study_streak_days: Consecutive days of study
        
    The statistics provide a quick overview of learning progress and engagement.
    """
    def get(self, request) -> Response:
        try:
            # Calculate success rate
            total_reviews = WordReviewItem.objects.count()
            if total_reviews > 0:
                correct_reviews = WordReviewItem.objects.filter(correct=True).count()
                success_rate = (correct_reviews / total_reviews * 100)
            else:
                success_rate = 0.0
            
            # Get total study sessions
            total_study_sessions = StudySession.objects.count()
            
            # Get total active groups (groups with at least one study session)
            total_active_groups = Group.objects.filter(
                study_sessions__isnull=False
            ).distinct().count()
            
            # Calculate study streak
            today = timezone.now().date()
            study_streak = 0
            
            # Get all study session dates ordered by date
            session_dates = StudySession.objects.values_list(
                'created_at', flat=True
            ).distinct().order_by('-created_at')
            
            if session_dates:
                # Convert to list and extract dates
                session_dates = [d.date() for d in session_dates]
                latest_date = session_dates[0]
                
                print(f"Today: {today}")
                print(f"Latest date: {latest_date}")
                print(f"All session dates: {session_dates}")
                
                # Only count streak if latest session is today
                if latest_date == today:
                    # Initialize streak to 1 for today
                    study_streak = 1
                    print(f"Found today's session, streak = {study_streak}")
                    
                    # Check consecutive days
                    for i in range(1, len(session_dates)):
                        current_date = session_dates[i-1]
                        next_date = session_dates[i]
                        diff = (current_date - next_date).days
                        print(f"Checking dates: {current_date} -> {next_date}, diff = {diff} days")
                        
                        # Check if this date is consecutive with the previous one
                        if diff == 1:
                            study_streak += 1
                            print(f"Consecutive day found, streak = {study_streak}")
                        else:
                            print(f"Gap found ({diff} days), breaking")
                            break
                else:
                    print(f"Latest session ({latest_date}) is not today ({today})")
            
            data = {
                'success_rate': round(success_rate, 1),
                'total_study_sessions': total_study_sessions,
                'total_active_groups': total_active_groups,
                'study_streak_days': study_streak
            }
            
            serializer = QuickStatsSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
