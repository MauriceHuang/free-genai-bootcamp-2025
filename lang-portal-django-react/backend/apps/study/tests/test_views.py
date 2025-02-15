import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from study.models import StudyActivity, StudySession, WordReviewItem
from words.models import Word, Group

@pytest.mark.django_db
class TestStudyActivityViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def activity(self):
        return StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )

    def test_list_activities(self, api_client, activity):
        url = reverse('studyactivity-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['items'][0]['name'] == "Test Activity"
        assert response.data['pagination']['total_items'] == 1

    def test_retrieve_activity(self, api_client, activity):
        url = reverse('studyactivity-detail', kwargs={'pk': activity.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Test Activity"
        assert response.data['thumbnail_url'] == "https://example.com/test.jpg"

    def test_activity_sessions(self, api_client, activity):
        group = Group.objects.create(name="Test Group")
        session = StudySession.objects.create(
            group=group,
            study_activity=activity
        )

        url = reverse('studyactivity-study-sessions', kwargs={'pk': activity.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['activity_name'] == "Test Activity"
        assert response.data['items'][0]['group_name'] == "Test Group"

    def test_activity_sessions_no_pagination(self, api_client, activity, monkeypatch):
        """Test the non-paginated response for study sessions"""
        group = Group.objects.create(name="Test Group")
        session = StudySession.objects.create(
            group=group,
            study_activity=activity
        )

        # Mock the paginate_queryset method to return None, forcing non-paginated response
        def mock_paginate_queryset(self, queryset):
            return None
        
        from study.views import StudyActivityViewSet
        monkeypatch.setattr(StudyActivityViewSet, 'paginate_queryset', mock_paginate_queryset)

        url = reverse('studyactivity-study-sessions', kwargs={'pk': activity.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Direct list, not paginated
        assert response.data[0]['activity_name'] == "Test Activity"
        assert response.data[0]['group_name'] == "Test Group"
        assert 'pagination' not in response.data

@pytest.mark.django_db
class TestStudySessionViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def session_data(self, db):
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        return {
            'group': group.id,
            'study_activity': activity.id
        }

    @pytest.fixture
    def session(self, session_data):
        activity = StudyActivity.objects.get(id=session_data['study_activity'])
        group = Group.objects.get(id=session_data['group'])
        return StudySession.objects.create(
            group=group,
            study_activity=activity
        )

    def test_create_session(self, api_client, session_data):
        url = reverse('studysession-list')
        response = api_client.post(url, session_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['group'] == session_data['group']
        assert response.data['study_activity'] == session_data['study_activity']

    def test_retrieve_session(self, api_client, session):
        url = reverse('studysession-detail', kwargs={'pk': session.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['activity_name'] == "Test Activity"
        assert response.data['group_name'] == "Test Group"
        assert 'review_items' in response.data

    def test_session_words(self, api_client, session):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        review = WordReviewItem.objects.create(
            word=word,
            study_session=session,
            correct=True
        )

        url = reverse('studysession-words', kwargs={'pk': session.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['word']['japanese'] == "テスト"

    def test_review_word(self, api_client, session):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )

        url = reverse('studysession-review-word', kwargs={
            'pk': session.pk,
            'word_id': word.pk
        })
        response = api_client.post(url, {'correct': True}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] is True
        assert response.data['word_id'] == word.pk
        assert response.data['study_session_id'] == session.pk
        assert response.data['correct'] is True

    def test_review_word_invalid(self, api_client, session):
        url = reverse('studysession-review-word', kwargs={
            'pk': session.pk,
            'word_id': 999  # Non-existent word
        })
        response = api_client.post(url, {'correct': True}, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
