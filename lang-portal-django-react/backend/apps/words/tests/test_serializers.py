import pytest
from words.models import Word, Group
from words.serializers import WordSerializer, GroupSerializer

@pytest.mark.django_db
class TestGroupSerializer:
    @pytest.fixture
    def group(self):
        return Group.objects.create(name="Test Group")

    def test_group_serialization(self, group):
        serializer = GroupSerializer(group)
        assert serializer.data == {
            'id': group.id,
            'name': 'Test Group',
            'word_count': 0
        }

@pytest.mark.django_db
class TestWordSerializer:
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

    def test_word_serialization(self, word, group):
        serializer = WordSerializer(word)
        assert serializer.data == {
            'japanese': 'テスト',
            'romaji': 'tesuto',
            'english': 'test',
            'stats': {
                'correct_count': 0,
                'wrong_count': 0
            },
            'groups': [{
                'id': group.id,
                'name': 'Test Group',
                'word_count': 1
            }]
        }

    def test_word_multiple_groups_serialization(self, word):
        another_group = Group.objects.create(name="Another Group")
        word.groups.add(another_group)

        serializer = WordSerializer(word)
        groups_data = serializer.data['groups']
        
        assert len(groups_data) == 2
        group_names = {group['name'] for group in groups_data}
        assert group_names == {'Test Group', 'Another Group'}
