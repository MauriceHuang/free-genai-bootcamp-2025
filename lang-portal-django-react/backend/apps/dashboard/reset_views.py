from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.management import call_command
from study.models import StudySession, WordReviewItem
from words.models import Word, Group

class ResetHistoryView(APIView):
    """
    Reset study history while preserving words and groups.
    
    This endpoint:
    - Clears all study sessions
    - Clears all word reviews
    - Preserves all words and groups
    
    Returns:
        Response with success message
    """
    def post(self, request):
        try:
            # Delete all word reviews first (due to foreign key constraint)
            WordReviewItem.objects.all().delete()
            
            # Delete all study sessions
            StudySession.objects.all().delete()
            
            return Response({
                "success": True,
                "message": "Study history has been reset"
            })
            
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FullResetView(APIView):
    """
    Perform a complete system reset.
    
    This endpoint:
    - Clears all data from the database
    - Reloads initial fixture data
    
    Returns:
        Response with success message
    """
    def post(self, request):
        try:
            # Flush the database (keeps structure but removes all data)
            call_command('flush', '--no-input')
            
            # Reload initial fixture data
            call_command('loaddata', 'fixtures/initial_data.json')
            
            return Response({
                "success": True,
                "message": "System has been fully reset"
            })
            
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 