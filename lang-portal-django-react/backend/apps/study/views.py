from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import StudyActivity, StudySession, WordReviewItem
from .serializers import (
    StudyActivitySerializer,
    StudySessionSerializer,
    StudySessionDetailSerializer,
    CreateStudySessionSerializer,
    WordReviewItemSerializer,
    WordReviewCreateSerializer
)

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'pagination': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'total_items': self.page.paginator.count,
                'items_per_page': self.page_size,
            }
        })

class StudyActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing study activities.
    """
    queryset = StudyActivity.objects.all()
    serializer_class = StudyActivitySerializer
    pagination_class = CustomPagination

    @action(detail=True, methods=['get'])
    def study_sessions(self, request, pk=None):
        """
        Get all study sessions for a specific activity.
        Endpoint: /api/study_activities/{id}/study_sessions/
        """
        activity = self.get_object()
        sessions = activity.sessions.all()
        page = self.paginate_queryset(sessions)
        
        if page is not None:
            serializer = StudySessionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = StudySessionSerializer(sessions, many=True)
        return Response(serializer.data)

class StudySessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing study sessions.
    """
    queryset = StudySession.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateStudySessionSerializer
        if self.action == 'retrieve':
            return StudySessionDetailSerializer
        return StudySessionSerializer

    @action(detail=True, methods=['get'])
    def words(self, request, pk=None):
        """
        Get all reviewed words for a specific study session.
        Endpoint: /api/study_sessions/{id}/words/
        """
        session = self.get_object()
        reviews = session.wordreviewitem_set.all()
        page = self.paginate_queryset(reviews)
        
        if page is not None:
            serializer = WordReviewItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = WordReviewItemSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='words/(?P<word_id>[^/.]+)/review')
    def review_word(self, request, pk=None, word_id=None):
        """
        Record a word review for the study session.
        Endpoint: /api/study_sessions/{id}/words/{word_id}/review/
        """
        serializer = WordReviewCreateSerializer(data={
            'word': word_id,
            'study_session': pk,
            'correct': request.data.get('correct', False)
        })
        
        if serializer.is_valid():
            review = serializer.save()
            return Response({
                'success': True,
                'word_id': review.word.id,
                'study_session_id': review.study_session.id,
                'correct': review.correct,
                'created_at': review.created_at
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
