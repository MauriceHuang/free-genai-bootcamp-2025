from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Word, Group
from .serializers import WordSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

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

class WordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    pagination_class = CustomPagination

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Add stats for single group view
        data['stats'] = {
            'total_word_count': instance.words.count()
        }
        return Response(data)

    @action(detail=True, methods=['get'])
    def words(self, request, pk=None):
        # This is a custom action endpoint that will be available at /api/groups/{id}/words/
        # The @action decorator creates an endpoint at /api/groups/{id}/words/
        # For example:
        # - /api/groups/1/words/ returns words for group with id=1
        # - /api/groups/42/words/ returns words for group with id=42
        
        # Get the specific group object based on the URL parameter
        group = self.get_object()
        
        # Get all words associated with this group
        words = group.words.all()
        
        # Try to paginate the words using the CustomPagination class
        # paginate_queryset() is a built-in DRF method inherited from GenericViewSet
        # It uses the pagination_class (CustomPagination) we defined above
        # For example:
        # - /api/groups/1/words/?page=1 returns first page of words
        # - /api/groups/1/words/?page=2 returns second page of words
        # Each page contains up to 100 words (defined in CustomPagination.page_size)
        # If no page parameter is provided, defaults to page=1
        page = self.paginate_queryset(words)
        
        if page is not None:
            # If pagination is successful, serialize only the words for the current page
            serializer = WordSerializer(page, many=True)
            # Return paginated response with pagination metadata
            return self.get_paginated_response(serializer.data)
            
        # If pagination is not used, serialize all words
        serializer = WordSerializer(words, many=True)
        # Return simple response with all words
        return Response(serializer.data)
