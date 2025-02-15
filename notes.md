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

## Next Steps

1. Implement remaining models:
   - StudySession
   - StudyActivity
   - WordReviewItem

2. Create remaining API endpoints:
   - Groups endpoints
   - Study sessions endpoints
   - Dashboard endpoints
   - Study activities endpoints

3. Add more comprehensive test data in fixtures

## Technical Notes

- Using Django 5.1.6 with Django REST Framework
- Custom pagination format implemented to match API spec
- CORS enabled for development
- SQLite database for development 