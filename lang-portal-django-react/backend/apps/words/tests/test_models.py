import pytest
from django.db import IntegrityError
from words.models import Word, Group

# Common pytest decorators:
# @pytest.mark.django_db - Enables database access for tests, handles test DB setup/teardown
#   Source: https://pytest-django.readthedocs.io/en/latest/database.html
# @pytest.fixture - Defines reusable test data/objects that can be injected into tests
#   Source: https://docs.pytest.org/en/stable/fixture.html
# @pytest.mark.parametrize - Runs same test multiple times with different parameters
#   Source: https://docs.pytest.org/en/stable/parametrize.html
# @pytest.mark.skip - Skips running this test
#   Source: https://docs.pytest.org/en/stable/skipping.html
# @pytest.mark.xfail - Marks test as expected to fail
#   Source: https://docs.pytest.org/en/stable/skipping.html#xfail-mark-test-functions-as-expected-to-fail
# @pytest.mark.timeout - Sets max time a test can run
#   Source: https://pypi.org/project/pytest-timeout/
@pytest.mark.django_db
class TestGroupModel:
    def test_group_creation(self):
        group = Group.objects.create(name="Test Group")
        assert group.name == "Test Group"
        assert str(group) == "Test Group"

    def test_group_name_required(self):
        with pytest.raises(IntegrityError):
            Group.objects.create(name=None)

@pytest.mark.django_db
class TestWordModel:
    @pytest.fixture
    def basic_group(self):
        return Group.objects.create(name="Basic Words")
    
    @pytest.fixture
    def common_group(self):
        return Group.objects.create(name="Common Phrases")

    def test_word_creation(self, basic_group):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        word.groups.add(basic_group)
        
        assert word.japanese == "テスト"
        assert word.romaji == "tesuto"
        assert word.english == "test"
        assert word.groups.count() == 1
        assert word.groups.first() == basic_group
        assert str(word) == "テスト (test)"

    def test_word_multiple_groups(self, basic_group, common_group):
        word = Word.objects.create(
            japanese="こんにちは",
            romaji="konnichiwa",
            english="hello"
        )
        word.groups.add(basic_group, common_group)
        
        assert word.groups.count() == 2
        assert set(word.groups.all()) == {basic_group, common_group}

    def test_word_stats_no_reviews(self, basic_group):
        word = Word.objects.create(
            japanese="テスト",
            romaji="tesuto",
            english="test"
        )
        word.groups.add(basic_group)
        
        stats = word.stats
        assert stats["correct_count"] == 0
        assert stats["wrong_count"] == 0

    def test_required_fields(self):
        with pytest.raises(IntegrityError):
            Word.objects.create(romaji="test", english="test")
        
        with pytest.raises(IntegrityError):
            Word.objects.create(japanese="テスト", english="test")
        
        with pytest.raises(IntegrityError):
            Word.objects.create(japanese="テスト", romaji="test")
