import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from words.models import Word, Group

@pytest.mark.django_db
class TestGroupViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def group(self):
        return Group.objects.create(name="Test Group")

    def test_list_groups(self, api_client, group):
        url = reverse('group-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['items'][0]['name'] == "Test Group"
        assert response.data['pagination']['total_items'] == 1

    def test_retrieve_group(self, api_client, group):
        url = reverse('group-detail', kwargs={'pk': group.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Test Group"
        assert 'stats' in response.data
        assert response.data['stats']['total_word_count'] == 0

    def test_group_words(self, api_client, group):
        # Create a word in the group
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        word.groups.add(group)

        url = reverse('group-words', kwargs={'pk': group.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['japanese'] == "テスト"

@pytest.mark.django_db
class TestWordViewSet:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def group(self):
        return Group.objects.create(name="Test Group")

    @pytest.fixture
    def word(self, group):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        word.groups.add(group)
        return word

    def test_list_words(self, api_client, word):
        url = reverse('word-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['japanese'] == "テスト"
        assert response.data['pagination']['total_items'] == 1

    def test_retrieve_word(self, api_client, word, group):
        url = reverse('word-detail', kwargs={'pk': word.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['japanese'] == "テスト"
        assert response.data['romaji'] == "tesuto"
        assert response.data['english'] == "test"
        assert len(response.data['groups']) == 1
        assert response.data['groups'][0]['name'] == "Test Group"

    def test_word_stats(self, api_client, word):
        url = reverse('word-detail', kwargs={'pk': word.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'stats' in response.data
        assert response.data['stats'] == {
            'correct_count': 0,
            'wrong_count': 0
        }
