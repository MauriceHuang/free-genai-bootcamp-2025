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

1. Implement Dashboard Features:
   - Create dashboard app endpoints:
     - `/api/dashboard/last_study_session`
     - `/api/dashboard/study_progress`
     - `/api/dashboard/quick-stats`
   - Implement success rate calculations
   - Add study streak tracking
   - Calculate total words studied vs. available

2. Add System Reset Functionality:
   - Implement `/api/reset_history` endpoint
     - Clear study sessions and word reviews
     - Preserve words and groups data
   - Implement `/api/full_reset` endpoint
     - Complete system reset
     - Reload initial fixture data

3. Enhance Testing:
   - Add tests for study app:
     - Test study activity model validations
     - Test session creation and word reviews
     - Test serializer edge cases
   - Add tests for dashboard features
   - Improve coverage for uncovered lines

4. Documentation and Code Quality:
   - Add API documentation for study activities
   - Document success/error response formats
   - Add input validation error messages
   - Review and standardize HTTP status codes

5. Frontend Integration Support:
   - Test all endpoints with frontend requirements
   - Verify timestamp formats
   - Ensure pagination works with frontend components
   - Add CORS headers for frontend development

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