import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from study.models import StudyActivity, StudySession, WordReviewItem
from words.models import Word, Group

@pytest.mark.django_db
class TestStudyActivityModel:
    def test_study_activity_creation(self):
        activity = StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        assert activity.name == "Test Activity"
        assert activity.thumbnail_url == "https://example.com/test.jpg"
        assert activity.description == "Test description"
        assert str(activity) == "Test Activity"

    def test_required_fields(self):
        # Test missing name
        activity = StudyActivity(
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )
        with pytest.raises(ValidationError):
            activity.full_clean()

        # Test missing thumbnail_url
        activity = StudyActivity(
            name="Test Activity",
            description="Test description"
        )
        with pytest.raises(ValidationError):
            activity.full_clean()

@pytest.mark.django_db
class TestStudySessionModel:
    @pytest.fixture
    def study_activity(self):
        return StudyActivity.objects.create(
            name="Test Activity",
            thumbnail_url="https://example.com/test.jpg",
            description="Test description"
        )

    @pytest.fixture
    def group(self):
        return Group.objects.create(name="Test Group")

    def test_study_session_creation(self, study_activity, group):
        session = StudySession.objects.create(
            group=group,
            study_activity=study_activity
        )
        assert session.group == group
        assert session.study_activity == study_activity
        assert session.created_at is not None
        assert session.end_time is None
        assert str(session) == f"{study_activity.name} - {group.name} ({session.created_at.strftime('%Y-%m-%d %H:%M')})"

    def test_review_items_count(self, study_activity, group):
        session = StudySession.objects.create(
            group=group,
            study_activity=study_activity
        )
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        
        # Create some review items
        WordReviewItem.objects.create(
            word=word,
            study_session=session,
            correct=True
        )
        WordReviewItem.objects.create(
            word=word,
            study_session=session,
            correct=False
        )
        
        assert session.review_items_count == 2

@pytest.mark.django_db
class TestWordReviewItemModel:
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
            study_activity=activity
        )

    @pytest.fixture
    def word(self, db):
        return Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )

    def test_word_review_creation(self, study_session, word):
        review = WordReviewItem.objects.create(
            word=word,
            study_session=study_session,
            correct=True
        )
        assert review.word == word
        assert review.study_session == study_session
        assert review.correct is True
        assert review.created_at is not None
        assert str(review) == f"{word.japanese} - ✓"

        # Test incorrect review
        review = WordReviewItem.objects.create(
            word=word,
            study_session=study_session,
            correct=False
        )
        assert str(review) == f"{word.japanese} - ✗"

    def test_required_fields(self, study_session, word):
        # Test missing word
        review = WordReviewItem(
            study_session=study_session,
            correct=True
        )
        with pytest.raises(ValidationError):
            review.full_clean()

        # Test missing study_session
        review = WordReviewItem(
            word=word,
            correct=True
        )
        with pytest.raises(ValidationError):
            review.full_clean()

        # Test missing correct flag
        review = WordReviewItem(
            word=word,
            study_session=study_session
        )
        with pytest.raises(ValidationError):
            review.full_clean()
