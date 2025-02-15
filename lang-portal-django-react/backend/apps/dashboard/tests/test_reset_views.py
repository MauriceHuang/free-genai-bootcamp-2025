import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.management import call_command

from study.models import StudySession, StudyActivity, WordReviewItem
from words.models import Word, Group

@pytest.mark.django_db
class TestResetHistoryView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def study_data(self):
        # Create test data
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        session = StudySession.objects.create(
            group=group,
            study_activity=activity
        )
        review = WordReviewItem.objects.create(
            word=word,
            study_session=session,
            correct=True
        )
        return {
            'group': group,
            'activity': activity,
            'word': word,
            'session': session,
            'review': review
        }

    def test_reset_history_success(self, api_client, study_data):
        # Verify initial data exists
        assert StudySession.objects.count() == 1
        assert WordReviewItem.objects.count() == 1
        assert Word.objects.count() > 0  # Initial data + our test word
        assert Group.objects.count() > 0  # Initial data + our test group

        # Make request to reset history
        url = reverse('reset-history')
        response = api_client.post(url)

        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['message'] == 'Study history has been reset'

        # Verify study history is cleared but words and groups remain
        assert StudySession.objects.count() == 0
        assert WordReviewItem.objects.count() == 0
        assert Word.objects.count() > 0  # Words should still exist
        assert Group.objects.count() > 0  # Groups should still exist

@pytest.mark.django_db
class TestFullResetView:
    @pytest.fixture(autouse=True)
    def setup_initial_data(self, db):
        # Load initial fixture data
        call_command('loaddata', 'fixtures/initial_data.json', verbosity=0)

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def study_data(self):
        # Create test data
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        session = StudySession.objects.create(
            group=group,
            study_activity=activity
        )
        review = WordReviewItem.objects.create(
            word=word,
            study_session=session,
            correct=True
        )
        return {
            'group': group,
            'activity': activity,
            'word': word,
            'session': session,
            'review': review
        }

    def test_full_reset_success(self, api_client, study_data):
        # Get initial counts from fixture data
        initial_word_count = 11  # From initial_data.json
        initial_group_count = 3   # From initial_data.json
        
        # Verify we have more than initial data (due to test data)
        assert StudySession.objects.count() > 0
        assert WordReviewItem.objects.count() > 0
        assert Word.objects.count() > initial_word_count
        assert Group.objects.count() > initial_group_count
        
        # Make request to perform full reset
        url = reverse('full-reset')
        response = api_client.post(url)

        # Check response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['message'] == 'System has been fully reset'

        # Verify study history is cleared
        assert StudySession.objects.count() == 0
        assert WordReviewItem.objects.count() == 0
        
        # Verify words and groups are reset to initial fixture data
        assert Word.objects.count() == initial_word_count
        assert Group.objects.count() == initial_group_count