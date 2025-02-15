from django.db import models
from words.models import Word, Group

class StudyActivity(models.Model):
    """
    Represents a type of study activity (e.g., Typing Exercise, Flashcards, etc.)
    """
    name = models.CharField(max_length=100)
    thumbnail_url = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Study activities"
        ordering = ['name']

    def __str__(self):
        return self.name

class StudySession(models.Model):
    """
    Represents a single study session where a user practices words from a group
    using a specific study activity.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='study_sessions')
    study_activity = models.ForeignKey(StudyActivity, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']  # Most recent sessions first

    def __str__(self):
        return f"{self.study_activity.name} - {self.group.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def review_items_count(self):
        return self.wordreviewitem_set.count()

class WordReviewItem(models.Model):
    """
    Represents a single review of a word during a study session.
    Records whether the user got the word correct or incorrect.
    """
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    study_session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.word.japanese} - {'✓' if self.correct else '✗'}"
