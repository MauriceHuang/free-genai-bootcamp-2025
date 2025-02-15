# Backend Server Technical Specs

## Business Goal:

A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

### Study Activities

The portal includes various study activities that help users practice vocabulary:

1. Typing Exercise
   - A frontend-focused activity where users practice typing Japanese words
   - Uses words from a selected group for practice
   - Flow:
     1. User selects a group of words to practice
     2. Frontend displays English meaning and expects Japanese input
     3. Each word attempt is recorded via `/api/study_sessions/:id/words/:word_id/review`
     4. Success/failure is tracked in WordReviewItem model
   - Backend Requirements:
     - No special endpoints needed beyond standard group words retrieval
     - Uses existing review tracking system
     - Relies on standard study session creation and word review endpoints
   
   Example API Flow:
   ```
   1. Start a new study session:
   POST /api/study_activities
   Request:
   {
     "group_id": 1,
     "study_activity_id": 1  // ID for typing exercise activity
   }
   Response:
   {
     "id": 124,  // new study session ID
     "group_id": 1
   }

   2. Get words for the group:
   GET /api/groups/1/words
   Response:
   {
     "items": [
       {
         "japanese": "こんにちは",
         "romaji": "konnichiwa",
         "english": "hello",
         "correct_count": 5,
         "wrong_count": 2
       }
       // ... more words
     ],
     "pagination": {...}
   }

   3. Record each word attempt:
   POST /api/study_sessions/124/words/1/review
   Request:
   {
     "correct": true  // or false based on user's input matching
   }
   Response:
   {
     "success": true,
     "word_id": 1,
     "study_session_id": 124,
     "correct": true,
     "created_at": "2025-02-08T17:33:07-05:00"
   }
   ```

## Technical Requirements

- The backend will be built using Python/Django
- The database will be SQLite3
- The API will be built using Django REST Framework (DRF)
- Django's built-in management commands will be used for tasks
- The API will always return JSON
- There will no authentication or authorization
- Everything be treated as a single user

## Directory Structure

```text
backend/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── core/                   # Main Django project directory
│   ├── __init__.py
│   ├── settings/          # Split settings for different environments
│   │   ├── __init__.py
│   │   ├── base.py       # Base settings shared across environments
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/                  # All Django applications
│   ├── __init__.py
│   ├── words/            # Main vocabulary app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py     # Word, WordGroup models
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_serializers.py
│   ├── study/            # Study sessions app
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py     # StudySession, StudyActivity models
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_serializers.py
│   └── dashboard/        # Dashboard specific endpoints
│       ├── __init__.py
│       ├── apps.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── tests/
│           ├── __init__.py
│           └── test_views.py
├── fixtures/             # Initial data for the database
│   ├── words.json
│   ├── groups.json
│   └── study_activities.json
├── utils/               # Shared utilities
│   ├── __init__.py
│   ├── constants.py
│   └── helpers.py
└── docs/               # API and development documentation
    ├── api.md
    └── development.md
```

## Database Schema

Our database will be defined in Django models within a `words` app. The database file will be `db.sqlite3` in the root of the project folder.

We have the following models:
- Word
  - id (AutoField)
  - japanese (CharField)
  - romaji (CharField)
  - english (CharField)
  - parts (JSONField)
- WordGroup (Many-to-Many relationship between Word and Group)
  - id (AutoField)
  - word (ForeignKey to Word)
  - group (ForeignKey to Group)
- Group
  - id (AutoField)
  - name (CharField)
- StudySession
  - id (AutoField)
  - group (ForeignKey to Group)
  - created_at (DateTimeField, auto_now_add=True)
  - study_activity (ForeignKey to StudyActivity)
- StudyActivity
  - id (AutoField)
  - study_session (ForeignKey to StudySession)
  - group (ForeignKey to Group)
  - created_at (DateTimeField, auto_now_add=True)
- WordReviewItem
  - word (ForeignKey to Word)
  - study_session (ForeignKey to StudySession)
  - correct (BooleanField)
  - created_at (DateTimeField, auto_now_add=True)

## API Endpoints

### GET /api/dashboard/last_study_session
Returns information about the most recent study session.

#### JSON Response
```json
{
  "id": 123,
  "group_id": 456,
  "created_at": "2025-02-08T17:20:23-05:00",
  "study_activity_id": 789,
  "group_id": 456,
  "group_name": "Basic Greetings"
}
```

### GET /api/dashboard/study_progress
Returns study progress statistics.
Please note that the frontend will determine progress bar based on total words studied and total available words.

#### JSON Response
```json
{
  "total_words_studied": 3,
  "total_available_words": 124,
}
```

### GET /api/dashboard/quick-stats
Returns quick overview statistics.

#### JSON Response
```json
{
  "success_rate": 80.0,
  "total_study_sessions": 4,
  "total_active_groups": 3,
  "study_streak_days": 4
}
```

### GET /api/study_activities/:id
#### JSON Response
```json
{
  "id": 1,
  "name": "Vocabulary Quiz",
  "thumbnail_url": "https://example.com/thumbnail.jpg",
  "description": "Practice your vocabulary with flashcards"
}
```

### GET /api/study_activities/:id/study_sessions
- pagination with 100 items per page using DRF's pagination classes

```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```

### POST /api/study_activities
#### Request Params
- group_id integer
- study_activity_id integer

#### JSON Response
```json
{
  "id": 124,
  "group_id": 123
}
```

### GET /api/words
- pagination with 100 items per page using DRF's pagination classes

#### JSON Response
```json
{
  "items": [
    {
      "japanese": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 500,
    "items_per_page": 100
  }
}
```

### GET /api/words/:id
#### JSON Response
```json
{
  "japanese": "こんにちは",
  "romaji": "konnichiwa",
  "english": "hello",
  "stats": {
    "correct_count": 5,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Basic Greetings"
    }
  ]
}
```

### GET /api/groups
- pagination with 100 items per page using DRF's pagination classes

#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "word_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id
#### JSON Response
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats": {
    "total_word_count": 20
  }
}
```

### GET /api/groups/:id/words
#### JSON Response
```json
{
  "items": [
    {
      "japanese": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id/study_sessions
#### JSON Response
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 5,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions
- pagination with 100 items per page using DRF's pagination classes

#### JSON Response
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions/:id
#### JSON Response
```json
{
  "id": 123,
  "activity_name": "Vocabulary Quiz",
  "group_name": "Basic Greetings",
  "start_time": "2025-02-08T17:20:23-05:00",
  "end_time": "2025-02-08T17:30:23-05:00",
  "review_items_count": 20
}
```

### GET /api/study_sessions/:id/words
- pagination with 100 items per page using DRF's pagination classes

#### JSON Response
```json
{
  "items": [
    {
      "japanese": "こんにちは",
      "romaji": "konnichiwa",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```

### POST /api/reset_history
#### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```

### POST /api/full_reset
#### JSON Response
```json
{
  "success": true,
  "message": "System has been fully reset"
}
```

### POST /api/study_sessions/:id/words/:word_id/review
#### Request Params
- id (study_session_id) integer
- word_id integer
- correct boolean

#### Request Payload
```json
{
  "correct": true
}
```

#### JSON Response
```json
{
  "success": true,
  "word_id": 1,
  "study_session_id": 123,
  "correct": true,
  "created_at": "2025-02-08T17:33:07-05:00"
}
```

## Django Management Commands

Let's list out possible management commands we need for our lang portal.

### Initialize Database
```bash
python manage.py migrate
```
This command will run all migrations and set up the database schema.

### Migrate Database
```bash
python manage.py makemigrations
python manage.py migrate
```
Migrations will be automatically managed by Django in the `migrations` folder of each app.

### Seed Data
```bash
python manage.py loaddata initial_data
```
This command will load data from JSON fixtures located in each app's `fixtures` directory.

The fixture files should follow Django's fixture format:
```json
[
  {
    "model": "words.word",
    "pk": 1,
    "fields": {
      "japanese": "払う",
      "romaji": "harau",
      "english": "to pay"
    }
  }
]
```