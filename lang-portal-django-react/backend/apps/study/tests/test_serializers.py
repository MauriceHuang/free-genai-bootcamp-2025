import pytest
from django.utils import timezone
from study.models import StudyActivity, StudySession, WordReviewItem
from study.serializers import (
    StudyActivitySerializer,
    StudySessionSerializer,
    StudySessionDetailSerializer,
    CreateStudySessionSerializer,
    WordReviewItemSerializer,
    WordReviewCreateSerializer
)
from words.models import Word, Group

@pytest.mark.django_db
class TestStudyActivitySerializer:
    @pytest.fixture
    def activity_data(self):
        return {
            'name': 'Test Activity',
            'thumbnail_url': 'https://example.com/test.jpg',
            'description': 'Test description'
        }

    def test_serialization(self, activity_data):
        activity = StudyActivity.objects.create(**activity_data)
        serializer = StudyActivitySerializer(activity)
        
        assert serializer.data['name'] == activity_data['name']
        assert serializer.data['thumbnail_url'] == activity_data['thumbnail_url']
        assert serializer.data['description'] == activity_data['description']

@pytest.mark.django_db
class TestStudySessionSerializer:
    @pytest.fixture
    def study_session(self, db):
        group = Group.objects.create(name="Test Group")
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        return StudySession.objects.create(
            group=group,
            study_activity=activity,
            end_time=timezone.now()
        )

    def test_basic_serialization(self, study_session):
        serializer = StudySessionSerializer(study_session)
        data = serializer.data
        
        assert data['id'] == study_session.id
        assert data['activity_name'] == study_session.study_activity.name
        assert data['group_name'] == study_session.group.name
        assert data['review_items_count'] == 0
        assert 'start_time' in data
        assert 'end_time' in data

    def test_detailed_serialization(self, study_session):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        review = WordReviewItem.objects.create(
            word=word,
            study_session=study_session,
            correct=True
        )

        serializer = StudySessionDetailSerializer(study_session)
        data = serializer.data
        
        assert 'review_items' in data
        assert len(data['review_items']) == 1
        assert data['review_items'][0]['word']['japanese'] == word.japanese
        assert data['review_items'][0]['correct'] is True

@pytest.mark.django_db
class TestCreateStudySessionSerializer:
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

    def test_create_session(self, session_data):
        serializer = CreateStudySessionSerializer(data=session_data)
        assert serializer.is_valid()
        
        session = serializer.save()
        assert session.group.id == session_data['group']
        assert session.study_activity.id == session_data['study_activity']

@pytest.mark.django_db
class TestWordReviewSerializers:
    @pytest.fixture
    def review_data(self, db):
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
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        return {
            'word': word.id,
            'study_session': session.id,
            'correct': True
        }

    def test_create_review(self, review_data):
        serializer = WordReviewCreateSerializer(data=review_data)
        assert serializer.is_valid()
        
        review = serializer.save()
        assert review.word.id == review_data['word']
        assert review.study_session.id == review_data['study_session']
        assert review.correct == review_data['correct']

    def test_review_serialization(self, review_data):
        serializer = WordReviewCreateSerializer(data=review_data)
        assert serializer.is_valid()
        review = serializer.save()

        read_serializer = WordReviewItemSerializer(review)
        data = read_serializer.data
        
        assert data['word']['japanese'] == "テスト"
        assert data['correct'] is True
        assert 'created_at' in data
