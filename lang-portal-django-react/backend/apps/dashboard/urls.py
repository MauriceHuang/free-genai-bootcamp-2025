from django.urls import path
from .views import LastStudySessionView, StudyProgressView, QuickStatsView
from .reset_views import ResetHistoryView, FullResetView

urlpatterns = [
    path('last-study-session/', LastStudySessionView.as_view(), name='last-study-session'),
    path('study-progress/', StudyProgressView.as_view(), name='study-progress'),
    path('quick-stats/', QuickStatsView.as_view(), name='quick-stats'),
    path('reset-history/', ResetHistoryView.as_view(), name='reset-history'),
    path('full-reset/', FullResetView.as_view(), name='full-reset'),
] 