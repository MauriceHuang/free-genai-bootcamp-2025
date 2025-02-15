# Language Portal Development Notes

## Implemented Features

### Backend (Django)

1. Models
   - Word model with fields:
     - japanese (CharField)
     - romaji (CharField)
     - english (CharField)
     - parts (JSONField)
     - groups (ManyToManyField to Group)
   - Group model with fields:
     - name (CharField)
   - StudyActivity model with fields:
     - name (CharField)
     - thumbnail_url (URLField)
     - description (TextField)
   - StudySession model with fields:
     - group (ForeignKey to Group)
     - study_activity (ForeignKey to StudyActivity)
     - created_at (DateTimeField)
     - end_time (DateTimeField)
   - WordReviewItem model with fields:
     - word (ForeignKey to Word)
     - study_session (ForeignKey to StudySession)
     - correct (BooleanField)
     - created_at (DateTimeField)

2. API Endpoints
   - `/api/words/`
     - GET: Returns paginated list of words with their groups and stats
     - Implements custom pagination with 100 items per page
   - `/api/words/{id}/`
     - GET: Returns detailed information about a specific word
   - `/api/groups/`
     - GET: Returns paginated list of groups with word counts
     - Implements custom pagination with 100 items per page
   - `/api/groups/{id}/`
     - GET: Returns detailed information about a specific group with stats
   - `/api/groups/{id}/words/`
     - GET: Returns paginated list of words in a specific group
   - `/api/` 
     - GET: Shows available API endpoints
   - `/api/study_activities/`
     - GET: Returns paginated list of available study activities
     ```json
     {
         "items": [
             {
                 "id": 1,
                 "name": "Typing Exercise",
                 "thumbnail_url": "https://example.com/thumbnails/typing.jpg",
                 "description": "Practice typing Japanese words..."
             }
         ],
         "pagination": {...}
     }
     ```
   - `/api/study_activities/{id}/study_sessions/`
     - GET: Returns paginated list of study sessions for an activity
     ```json
     {
         "items": [
             {
                 "id": 1,
                 "activity_name": "Typing Exercise",
                 "group_name": "Basic Greetings",
                 "start_time": "2025-02-08T22:20:23Z",
                 "end_time": "2025-02-08T22:30:23Z",
                 "review_items_count": 3
             }
         ],
         "pagination": {...}
     }
     ```
   - `/api/study_sessions/`
     - GET: Returns paginated list of all study sessions
     - POST: Creates a new study session
       ```json
       Request:
       {
           "group": 3,
           "study_activity": 1
       }
       ```
   - `/api/study_sessions/{id}/`
     - GET: Returns detailed information about a study session including word reviews
     ```json
     {
         "id": 1,
         "activity_name": "Typing Exercise",
         "group_name": "Basic Greetings",
         "start_time": "2025-02-08T22:20:23Z",
         "end_time": "2025-02-08T22:30:23Z",
         "review_items_count": 3,
         "review_items": [
             {
                 "word": {
                     "japanese": "こんにちは",
                     "romaji": "konnichiwa",
                     "english": "hello",
                     "stats": {...},
                     "groups": [...]
                 },
                 "correct": true,
                 "created_at": "2025-02-08T22:21:00Z"
             }
         ]
     }
     ```
   - `/api/study_sessions/{id}/words/{word_id}/review/`
     - POST: Records a word review for the session
     ```json
     Request:
     {
         "correct": true
     }
     Response:
     {
         "success": true,
         "word_id": 9,
         "study_session_id": 3,
         "correct": true,
         "created_at": "2025-02-15T13:51:31.800779Z"
     }
     ```

3. Data
   - Initial fixture data loaded with:
     - Basic Greetings group
     - Sample word "こんにちは" (konnichiwa)
   - Fixture Loading Process:
     ```bash
     # Location: lang-portal-django-react/backend/fixtures/initial_data.json
     # Format:
     [
         {
             "model": "words.group",
             "pk": 1,
             "fields": {
                 "name": "Basic Greetings"
             }
         },
         {
             "model": "words.word",
             "pk": 1,
             "fields": {
                 "japanese": "こんにちは",
                 "romaji": "konnichiwa",
                 "english": "hello",
                 "parts": null,
                 "groups": [1]
             }
         }
     ]

     # Load command:
     python manage.py loaddata fixtures/initial_data.json
     ```

## Testing API Endpoints

1. Start the Development Server:
   ```bash
   # Navigate to backend directory
   cd lang-portal-django-react/backend
   
   # Start the server
   python manage.py runserver
   ```

2. Test Endpoints Using curl:
   ```bash
   # Test API root
   curl http://127.0.0.1:8000/api/ | python -m json.tool

   # Test words list endpoint
   # -H flag sets HTTP headers. "Accept: application/json" tells the server we want JSON response
   curl -H "Accept: application/json" http://127.0.0.1:8000/api/words/ | python -m json.tool

   # Test single word endpoint
   curl -H "Accept: application/json" http://127.0.0.1:8000/api/words/1/ | python -m json.tool

   # Test groups list endpoint
   curl -H "Accept: application/json" http://127.0.0.1:8000/api/groups/ | python -m json.tool

   # Test single group endpoint
   curl -H "Accept: application/json" http://127.0.0.1:8000/api/groups/1/ | python -m json.tool

   # Test group words endpoint
   curl -H "Accept: application/json" http://127.0.0.1:8000/api/groups/1/words/ | python -m json.tool
   ```

3. Expected Responses:
   - API Root:
     ```json
     {
         "words": "http://127.0.0.1:8000/api/words/",
         "groups": "http://127.0.0.1:8000/api/groups/"
     }
     ```
   - Words List:
     ```json
     {
         "items": [
             {
                 "japanese": "こんにちは",
                 "romaji": "konnichiwa",
                 "english": "hello",
                 "stats": {
                     "correct_count": 0,
                     "wrong_count": 0
                 },
                 "groups": [
                     {
                         "id": 1,
                         "name": "Basic Greetings"
                     }
                 ]
             }
         ],
         "pagination": {
             "current_page": 1,
             "total_pages": 1,
             "total_items": 1,
             "items_per_page": 100
         }
     }
     ```
   - Groups List:
     ```json
     {
         "items": [
             {
                 "id": 1,
                 "name": "Basic Greetings",
                 "word_count": 1
             }
         ],
         "pagination": {
             "current_page": 1,
             "total_pages": 1,
             "total_items": 1,
             "items_per_page": 100
         }
     }
     ```
   - Single Group:
     ```json
     {
         "id": 1,
         "name": "Basic Greetings",
         "word_count": 1,
         "stats": {
             "total_word_count": 1
         }
     }
     ```
   - Group Words:
     ```json
     {
         "items": [
             {
                 "japanese": "こんにちは",
                 "romaji": "konnichiwa",
                 "english": "hello",
                 "stats": {
                     "correct_count": 0,
                     "wrong_count": 0
                 },
                 "groups": [
                     {
                         "id": 1,
                         "name": "Basic Greetings"
                     }
                 ]
             }
         ],
         "pagination": {
             "current_page": 1,
             "total_pages": 1,
             "total_items": 1,
             "items_per_page": 100
         }
     }
     ```

4. Browser Testing:
   - Visit `http://127.0.0.1:8000/api/` in a web browser
   - Django REST Framework provides a browsable API interface

## Data Management Options

1. Django Admin Interface:
   - Register models in admin.py
   - Access via http://127.0.0.1:8000/admin/
   - User-friendly interface for CRUD operations
   - Requires superuser account

2. Django Management Commands:
   - Create custom commands in words/management/commands/
   - Can write scripts to import data from various sources
   - Example uses:
     - Import from CSV/Excel files
     - Scrape data from language learning websites
     - Batch create/update operations

3. Django Shell:
   - Use `python manage.py shell`
   - Interactive Python environment with Django models loaded
   - Good for testing and one-off data operations
   - Can use iPython for better interface

4. Additional Fixtures:
   - Create multiple JSON fixture files
   - Organize by categories (e.g., basic_words.json, intermediate_words.json)
   - Can split data by groups or difficulty levels

5. API Endpoints:
   - Could add POST/PUT endpoints for data creation
   - Useful for future admin interface or data management tools
   - Would need to modify current read-only viewsets

6. Database GUI Tools:
   - Use SQLite browser tools
   - Direct database manipulation
   - Useful for bulk operations
   - Be careful with relationships and constraints

## Database Reset and Fixture Loading

1. Clear Database (Complete Reset):
   ```bash
   python manage.py flush  # Removes all data but keeps structure
   python manage.py loaddata fixtures/initial_data.json  # Reload fixtures
   ```

2. Backup Existing Data:
   ```bash
   python manage.py dumpdata words > backup.json  # Backup specific app
   python manage.py dumpdata > full_backup.json   # Backup everything
   ```

3. Loaddata Behavior:
   - Uses primary keys (PKs) from fixture files
   - Updates existing records if PKs match
   - Creates new records if PKs don't exist
   - No automatic duplicate detection
   - Safe to run multiple times (will update rather than duplicate)
   - Many-to-Many Relationships:
     ```json
     {
         "model": "words.word",
         "pk": 12,
         "fields": {
             "japanese": "おやすみなさい",
             "romaji": "oyasuminasai",
             "english": "good night",
             "parts": null,
             "groups": [1, 2]  // Word belongs to multiple groups
         }
     }
     ```
     - Groups field takes an array of group IDs
     - When loading: removes existing relationships, creates new ones
     - Can add to multiple groups without affecting other words
     - Order of loading doesn't matter (Django handles relationships after all models loaded)

4. Best Practices:
   - Backup data before major changes
   - Use consistent PKs across fixture files
   - Keep fixture files organized by category
   - Document any dependencies between fixtures

## Next Steps

1. Add System Reset Functionality:
   - Implement `/api/reset_history` endpoint
     - Clear study sessions and word reviews
     - Preserve words and groups data
   - Implement `/api/full_reset` endpoint
     - Complete system reset
     - Reload initial fixture data

## Technical Notes

- Using Django 5.1.6 with Django REST Framework
- Custom pagination format implemented to match API spec
- CORS enabled for development
- SQLite database for development 

## Testing

1. Test Structure:
   ```
   backend/apps/words/tests/
   ├── __init__.py
   ├── test_models.py      # Tests for Word and Group models
   ├── test_serializers.py # Tests for serializers
   └── test_views.py       # Tests for API endpoints

   backend/apps/study/tests/
   ├── __init__.py
   ├── test_models.py      # Tests for StudyActivity, StudySession, and WordReviewItem models
   ├── test_serializers.py # Tests for serializers
   └── test_views.py       # Tests for API endpoints
   ```

2. Running Tests:
   ```bash
   # Install test dependencies
   pip install pytest pytest-django pytest-cov

   # Run all tests with coverage report
   python -m pytest

   # Run specific test file
   python -m pytest apps/words/tests/test_models.py

   # Run specific test class
   python -m pytest apps/words/tests/test_models.py::TestWordModel

   # Run specific test method
   python -m pytest apps/words/tests/test_models.py::TestWordModel::test_word_creation

   # Run tests for a specific app
   python -m pytest apps/dashboard/tests/test_views.py

   # Run specific test class in an app
   python -m pytest apps/dashboard/tests/test_views.py::TestQuickStatsView

   # Run with coverage for specific app
   python -m pytest apps/dashboard/tests/test_views.py --cov=apps.dashboard

   # Run with coverage and show missing lines
   python -m pytest --cov=apps --cov-report=term-missing
   ```

3. Test Coverage (as of 2025-02-15):
   - Overall Coverage: 98%
   - Models: 100% coverage
     - StudyActivity model tests
     - StudySession model tests
     - WordReviewItem model tests
   - Serializers: 100% coverage
     - Basic and detailed serialization
     - Creation serializers
     - Nested data handling
   - Views: 94-100% coverage
     - Paginated and non-paginated responses
     - CRUD operations
     - Custom actions
     - Error handling

4. Test Configuration:
   ```ini
   # pytest.ini
   [pytest]
   DJANGO_SETTINGS_MODULE = core.settings
   python_files = test_*.py
   addopts = --cov=apps --cov-report=term-missing
   ```

5. Recent Improvements:
   - Added test for non-paginated responses in StudyActivityViewSet
   - Improved test documentation with detailed comments
   - Added monkeypatch usage for pagination control
   - Verified edge cases in API responses

6. Current Test Status:
   - Total Tests: 36
   - Passing: 36
   - Coverage by App:
     - study: 94-100%
     - words: 90-100%
     - dashboard: Pending implementation

7. Testing Best Practices Implemented:
   - Using fixtures for common test data
   - Testing both success and error cases
   - Proper isolation using @pytest.mark.django_db
   - Comprehensive model validation testing
   - API response structure verification
   - Pagination handling verification

8. Areas for Improvement:
   - Dashboard app tests need implementation
   - Add more edge cases for error handling
   - Improve test documentation
   - Add performance tests for large datasets
   - Add integration tests between apps

9. Common pytest decorators in use:
   ```python
   @pytest.mark.django_db
   # Enables database access for tests, handles test DB setup/teardown
   # Use case: When testing model creation, queries, or any database operations
   # Example: Testing Word model creation and relationships with Groups
   
   @pytest.fixture 
   # Defines reusable test data/objects that can be injected into tests
   # Use case: Creating test data that's needed across multiple tests
   # Example: Creating a test Group object that multiple Word tests can use
   
   @pytest.mark.parametrize
   # Runs same test multiple times with different parameters
   # Use case: Testing function behavior with multiple input variations
   # Example: Testing word validation with different invalid inputs
   
   @pytest.mark.skip
   # Skips running this test
   # Use case: Temporarily skipping tests that are broken or in development
   
   @pytest.mark.xfail
   # Marks test as expected to fail
   # Use case: Documenting known bugs or unimplemented features
   ```

6. Testing Model Validation:
   ```python
   # Testing required fields using ValidationError
   def test_required_fields(self):
       # Create word instance without required field
       word = Word(romaji="test", english="test")  # missing japanese field
       
       # Validate using full_clean()
       with pytest.raises(ValidationError):
           word.full_clean()
   ```

7. Testing Best Practices:
   - Use `full_clean()` for model validation instead of just saving
   - Use `ValidationError` for field validation tests
   - Use `IntegrityError` for database constraint tests
   - Create fixtures for commonly used test data
   - Test both success and failure cases
   - Keep tests focused and well-named
   - Add comments explaining complex test scenarios

8. Current Test Status:
   - Total Coverage: 98%
   - Test Suite Status:
     - Total Tests: 36
     - All tests passing
     - No skipped or xfailed tests
   - Coverage by Component:
     - Models: 100% coverage (study and words apps)
     - Serializers: 100% coverage (all serializer classes)
     - Views: 94-100% coverage
       - StudyActivityViewSet: 100% (including non-paginated responses)
       - StudySessionViewSet: 94% (missing some error cases)
       - WordViewSet: 100%
       - GroupViewSet: 100%
   - Specific Coverage Gaps:
     - study/views.py: Lines 69, 85-86 (error handling)
     - words/models.py: Lines 37-38 (stats edge cases)
     - words/serializers.py: Lines 25-26 (error handling)
   - Recent Coverage Improvements:
     - Added non-paginated response testing
     - Improved error case handling
     - Added comprehensive model validation tests

10. DateTime Handling in Tests:

    a. Issue Description:
    There were two main problems with datetime handling in tests:

    1. **Date Creation Issue:**
    When creating test sessions with explicit dates, setting `created_at` directly didn't work:
    ```python
    # Original problematic code
    session = StudySession.objects.create(
        group=group,
        study_activity=activity,
        created_at=session_date  # This doesn't work as expected
    )
    ```

    This failed because Django's `auto_now_add=True` on the `created_at` field would override any value we tried to set. Example of the issue:
    ```python
    # What we wanted:
    Session 1: created_at = 2025-02-15 12:00:00+00:00  # Today
    Session 2: created_at = 2025-02-14 12:00:00+00:00  # Yesterday
    Session 3: created_at = 2025-02-13 12:00:00+00:00  # 2 days ago

    # What we actually got:
    Session 1: created_at = 2025-02-15 12:00:00+00:00  # All sessions
    Session 2: created_at = 2025-02-15 12:00:00+00:00  # got the same
    Session 3: created_at = 2025-02-15 12:00:00+00:00  # creation date
    ```

    2. **Timezone Handling:**
    The code was mixing timezone-aware and naive datetime objects:
    ```python
    base_date = datetime(2025, 2, 15, 12, 0, tzinfo=dt_timezone.utc)  # Explicit timezone
    session_date = base_date - timedelta(days=1)  # This preserves timezone
    today = timezone.now().date()  # This uses system timezone
    ```

    b. The Fix:
    1. **Using `freeze_time` for Date Creation:**
    Instead of setting `created_at` directly, we use `freeze_time` to set the system time when creating each session:
    ```python
    # Fixed code
    base_date = timezone.now()  # 2025-02-15 12:00:00+00:00

    # Create sessions with explicit dates
    session_dates = [
        base_date,                          # 2025-02-15 12:00:00+00:00
        base_date - timedelta(days=1),      # 2025-02-14 12:00:00+00:00
        base_date - timedelta(days=2)       # 2025-02-13 12:00:00+00:00
    ]

    for session_date in session_dates:
        with freeze_time(session_date):
            session = StudySession.objects.create(
                group=group,
                study_activity=activity
            )
    ```

    This ensures correct creation dates:
    ```python
    # What we now get (correct dates):
    Session 1: created_at = 2025-02-15 12:00:00+00:00  # Today
    Session 2: created_at = 2025-02-14 12:00:00+00:00  # Yesterday
    Session 3: created_at = 2025-02-13 12:00:00+00:00  # 2 days ago
    ```

    2. **Consistent Timezone Usage:**
    We now use Django's `timezone.now()` consistently:
    ```python
    base_date = timezone.now()  # Always timezone-aware
    today = timezone.now().date()  # Date-only but from same timezone
    ```

    c. Benefits of the Fix:
    1. Each session gets the correct creation date
    2. Streak calculation works correctly by properly detecting consecutive days
    3. All datetime comparisons use timezone-aware objects
    4. Tests are deterministic and repeatable with fixed time points

    The result is accurate streak calculation that correctly identifies 3 consecutive days of study when sessions are created on 2025-02-13, 2025-02-14, and 2025-02-15.

## Study Activities Implementation

1. Models:
   - StudyActivity: Represents different types of study activities
   - StudySession: Tracks individual study sessions
   - WordReviewItem: Records individual word reviews

2. Features:
   - Custom pagination (100 items per page)
   - Detailed serializers for different use cases
   - Nested resource access (sessions within activities, reviews within sessions)
   - Proper timestamp handling for session tracking

3. Manual Testing Results (2025-02-15):
   ```
   [13:50:44] "GET /api/study_activities/" 200 513
   [13:50:53] "GET /api/study_activities/1/study_sessions/" 200 429
   [13:51:02] "GET /api/study_sessions/1/" 200 963
   [13:51:15] "POST /api/study_sessions/" 201 30
   [13:51:31] "POST /api/study_sessions/3/words/9/review/" 200 107
   ```
   All endpoints working as expected with proper response codes and data.

## Dashboard Implementation

1. Architecture Decisions:
   - Using `APIView` instead of `ViewSet` for dashboard endpoints
     - Simpler implementation for statistic-focused endpoints
     - No need for full REST operations (list/retrieve/create/update/delete)
     - More focused, single-purpose endpoints
     - Trade-off: Endpoints don't show up in API root listing

2. Django REST Framework View Types (Source: https://www.django-rest-framework.org/api-guide/views/):

   a. APIView
      - Base class for all DRF views
      - Direct mapping to HTTP methods (get, post, put, delete)
      - Use cases:
        - Custom endpoints with specific business logic
        - Statistical endpoints (like our dashboard)
        - Non-CRUD operations
        - Complex data aggregation
      Example from our dashboard:
      ```python
      class QuickStatsView(APIView):
          def get(self, request):
              # Custom logic for calculating statistics
              return Response(stats_data)
      ```

   b. ViewSet
      - Combines common operations into a single class
      - Automatically handles URL routing
      - Built-in support for DRF's Router class
      - Use cases:
        - CRUD operations on models
        - Standard REST APIs
        - Resource-based views
      Example from our words app:
      ```python
      class WordViewSet(viewsets.ReadOnlyModelViewSet):
          queryset = Word.objects.all()
          serializer_class = WordSerializer
      ```

   c. GenericAPIView
      - Adds common REST functionality to APIView
      - Includes pagination, filtering, and sorting
      - Use cases:
        - When you need some but not all ViewSet features
        - Custom list/detail views with standard behaviors
      Example:
      ```python
      class WordListView(generics.ListAPIView):
          queryset = Word.objects.all()
          serializer_class = WordSerializer
          pagination_class = CustomPagination
      ```

   d. Generic ViewSets (Source: https://www.django-rest-framework.org/api-guide/viewsets/):
      - ModelViewSet: Full CRUD operations
      - ReadOnlyModelViewSet: List and retrieve only
      - Use cases:
        - Standard database operations
        - When you need automatic URL routing
      Example:
      ```python
      class GroupViewSet(viewsets.ReadOnlyModelViewSet):
          queryset = Group.objects.all()
          serializer_class = GroupSerializer
      ```

3. Choosing Between View Types:

   a. Use APIView when:
      - You need complete control over behavior
      - Implementing custom endpoints
      - Building non-CRUD functionality
      - Handling complex business logic

   b. Use ViewSet when:
      - Working with standard CRUD operations
      - Need automatic URL routing
      - Want to minimize boilerplate code
      - Building resource-oriented APIs

   c. Use GenericAPIView when:
      - You need specific generic views
      - Want pagination/filtering without ViewSet
      - Building custom list/detail views

   d. Use Generic ViewSets when:
      - Need quick CRUD implementation
      - Working directly with models
      - Want maximum automation

4. Current Implementation Examples:

   a. Dashboard (APIView):
   ```python
   # Custom statistical endpoint
   class QuickStatsView(APIView):
       def get(self, request):
           return Response({
               "success_rate": 83.3,
               "total_study_sessions": 3,
               "total_active_groups": 2,
               "study_streak_days": 3
           })
   ```

   b. Words (ViewSet):
   ```python
   # Standard CRUD operations
   class WordViewSet(viewsets.ReadOnlyModelViewSet):
       queryset = Word.objects.all()
       serializer_class = WordSerializer
   ```

5. URL Patterns:

   a. APIView URLs (explicit):
   ```python
   urlpatterns = [
       path('quick-stats/', QuickStatsView.as_view()),
   ]
   ```

   b. ViewSet URLs (router-based):
   ```python
   router = DefaultRouter()
   router.register(r'words', WordViewSet)
   urlpatterns = router.urls
   ```

6. Endpoints Implementation:
   ```python
   # Using APIView for focused, statistic-based endpoints
   class QuickStatsView(APIView):
       def get(self, request):
           # Returns: success_rate, total_study_sessions, 
           # total_active_groups, study_streak_days
   
   class StudyProgressView(APIView):
       def get(self, request):
           # Returns: total_words_studied, total_available_words
   
   class LastStudySessionView(APIView):
       def get(self, request):
           # Returns: session details including activity_name, 
           # group_name, timing, and review count
   ```

7. URL Structure:
   ```python
   # Direct URL patterns instead of router registration
   urlpatterns = [
       path('last-study-session/', LastStudySessionView.as_view()),
       path('study-progress/', StudyProgressView.as_view()),
       path('quick-stats/', QuickStatsView.as_view()),
   ]
   ```

8. API Endpoints:
   - GET `/api/dashboard/quick-stats/`
     ```json
     {
         "success_rate": 83.3,
         "total_study_sessions": 3,
         "total_active_groups": 2,
         "study_streak_days": 3
     }
     ```
   - GET `/api/dashboard/study-progress/`
     ```json
     {
         "total_words_studied": 4,
         "total_available_words": 11
     }
     ```
   - GET `/api/dashboard/last-study-session/`
     ```json
     {
         "id": 1,
         "activity_name": "Typing Exercise",
         "group_name": "Basic Greetings",
         "created_at": "2025-02-15T14:00:00Z",
         "end_time": "2025-02-15T14:10:00Z",
         "review_items_count": 2
     }
     ```

9. Note on API Root:
   - Dashboard endpoints don't appear in `/api/` root listing
   - This is because they use `APIView` instead of `ViewSet`
   - API root only shows router-registered endpoints:
     ```json
     {
         "words": "http://127.0.0.1:8000/api/words/",
         "groups": "http://127.0.0.1:8000/api/groups/",
         "study_activities": "http://127.0.0.1:8000/api/study_activities/",
         "study_sessions": "http://127.0.0.1:8000/api/study_sessions/"
     }
     ```

10. Testing:
    - Manual testing with curl:
      ```bash
      # Test quick stats
      curl -H "Accept: application/json" http://127.0.0.1:8000/api/dashboard/quick-stats/
      
      # Test study progress
      curl -H "Accept: application/json" http://127.0.0.1:8000/api/dashboard/study-progress/
      
      # Test last study session
      curl -H "Accept: application/json" http://127.0.0.1:8000/api/dashboard/last-study-session/
      ```
    - Test data provided in fixtures/dashboard_test_data.json
    - All endpoints return proper JSON responses
    - Statistics calculated correctly based on test data

11. Testing Resets:
    - Reload fixture data:
      ```sh
      python manage.py loaddata fixtures/initial_data.json fixtures/study_activities.json fixtures/additional_data.json
      ```

    - Verify data was loaded:
      ```sh
      python manage.py shell -c "from words.models import Word, Group; from study.models import StudyActivity, StudySession, WordReviewItem; print(f'Words: {Word.objects.count()}\nGroups: {Group.objects.count()}\nStudy Activities: {StudyActivity.objects.count()}\nStudy Sessions: {StudySession.objects.count()}\nWord Reviews: {WordReviewItem.objects.count()}')"
      ```

    - Expected output:
      ```sh
      Words: 12
      Groups: 3 
      Study Activities: 2
      Study Sessions: 3
      Word Reviews: 6
      ```

    - Data loaded successfully:
      - 12 words (11 from initial_data.json + 1 from additional_data.json)
      - 3 groups (from initial_data.json)
      - 2 study activities
      - 3 study sessions 
      - 6 word reviews

    - Reset endpoint behavior:
      - `/api/reset-history/`: Preserves words and groups, no reload needed
      - `/api/full-reset/`: Automatically reloads initial_data.json
        - For complete dataset, run loaddata command shown above