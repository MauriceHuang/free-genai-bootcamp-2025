import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone
from freezegun import freeze_time

from study.models import StudySession, StudyActivity, WordReviewItem
from words.models import Word, Group

@pytest.mark.django_db
class TestLastStudySessionView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def study_session(self):
        # Create required related objects
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        # Create study session
        return StudySession.objects.create(
            group=group,
            study_activity=activity,
            end_time=timezone.now()
        )

    def test_get_last_session_success(self, api_client, study_session):
        url = reverse('last-study-session')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['activity_name'] == "Test Activity"
        assert response.data['group_name'] == "Test Group"
        assert 'created_at' in response.data
        assert 'end_time' in response.data
        assert response.data['review_items_count'] == 0

    def test_get_last_session_empty(self, api_client):
        url = reverse('last-study-session')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == "No study sessions found"

    def test_get_last_session_with_reviews(self, api_client, study_session):
        # Create a word and review
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        WordReviewItem.objects.create(
            word=word,
            study_session=study_session,
            correct=True
        )

        url = reverse('last-study-session')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['review_items_count'] == 1

@pytest.mark.django_db
class TestStudyProgressView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def study_data(self):
        # Create words
        word1 = Word.objects.create(
            japanese="テスト1",
            romaji="tesuto1",
            english="test1"
        )
        word2 = Word.objects.create(
            japanese="テスト2",
            romaji="tesuto2",
            english="test2"
        )
        
        # Create study session
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        session = StudySession.objects.create(
            group=group,
            study_activity=activity
        )
        
        # Create review for word1 only
        WordReviewItem.objects.create(
            word=word1,
            study_session=session,
            correct=True
        )
        
        return {'word1': word1, 'word2': word2, 'session': session}

    def test_get_study_progress_success(self, api_client, study_data):
        url = reverse('study-progress')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_words_studied'] == 1  # Only word1 was studied
        assert response.data['total_available_words'] == 2  # Total words in system

    def test_get_study_progress_empty(self, api_client):
        url = reverse('study-progress')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_words_studied'] == 0
        assert response.data['total_available_words'] == 0

@pytest.mark.django_db
class TestQuickStatsView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    @freeze_time("2025-02-15 12:00:00")
    def study_data(self):
        # Create groups
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        
        # Create activity
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        
        # Create sessions for the last 3 days with specific dates
        sessions = []
        base_date = timezone.now()
        
        # Create sessions with explicit dates
        session_dates = [
            base_date,  # today
            base_date - timedelta(days=1),  # yesterday
            base_date - timedelta(days=2)  # 2 days ago
        ]
        
        for i, session_date in enumerate(session_dates):
            with freeze_time(session_date):
                session = StudySession.objects.create(
                    group=group1 if i % 2 == 0 else group2,
                    study_activity=activity
                )
                sessions.append(session)
        
        # Create word and reviews
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        
        # Create 4 reviews: 3 correct, 1 incorrect (75% success rate)
        WordReviewItem.objects.create(
            word=word,
            study_session=sessions[0],
            correct=True
        )
        WordReviewItem.objects.create(
            word=word,
            study_session=sessions[0],
            correct=True
        )
        WordReviewItem.objects.create(
            word=word,
            study_session=sessions[1],
            correct=True
        )
        WordReviewItem.objects.create(
            word=word,
            study_session=sessions[2],
            correct=False
        )
        
        return {
            'groups': [group1, group2],
            'sessions': sessions,
            'word': word,
            'today': base_date
        }

    @freeze_time("2025-02-15 12:00:00")
    def test_get_quick_stats_success(self, api_client, study_data):
        url = reverse('quick-stats')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success_rate'] == 75.0  # 3 correct out of 4 reviews
        assert response.data['total_study_sessions'] == 3
        assert response.data['total_active_groups'] == 2
        assert response.data['study_streak_days'] == 3

    def test_get_quick_stats_empty(self, api_client):
        url = reverse('quick-stats')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success_rate'] == 0.0
        assert response.data['total_study_sessions'] == 0
        assert response.data['total_active_groups'] == 0
        assert response.data['study_streak_days'] == 0

    @freeze_time("2025-02-15 12:00:00")
    def test_get_quick_stats_broken_streak(self, api_client):
        # Create session from 3 days ago
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        
        # Create a session 3 days ago with explicit date
        base_date = timezone.now()
        session_date = base_date - timedelta(days=3)
        
        with freeze_time(session_date):
            StudySession.objects.create(
                group=group,
                study_activity=activity
            )
        
        url = reverse('quick-stats')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['study_streak_days'] == 0  # Streak broken
