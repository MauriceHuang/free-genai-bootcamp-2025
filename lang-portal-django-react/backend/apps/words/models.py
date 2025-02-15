from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Word(models.Model):
    japanese = models.CharField(max_length=100)
    romaji = models.CharField(max_length=100)
    english = models.CharField(max_length=100)
    parts = models.JSONField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='words')

    def __str__(self):
        return f"{self.japanese} ({self.english})"
    
    @property
    def stats(self):
        try:
            # Calculate stats from WordReviewItem
            correct_reviews = self.wordreviewitem_set.filter(correct=True).count()
            wrong_reviews = self.wordreviewitem_set.filter(correct=False).count()
            return {
                "correct_count": correct_reviews,
                "wrong_count": wrong_reviews
            }
        except AttributeError:
            return {
                "correct_count": 0,
                "wrong_count": 0
            }
