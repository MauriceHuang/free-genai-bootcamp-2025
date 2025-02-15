from django.urls import path
from .views import LastStudySessionView, StudyProgressView, QuickStatsView

urlpatterns = [
    path('last-study-session/', LastStudySessionView.as_view(), name='last-study-session'),
    path('study-progress/', StudyProgressView.as_view(), name='study-progress'),
    path('quick-stats/', QuickStatsView.as_view(), name='quick-stats'),
]