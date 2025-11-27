# PaperLight - Flask

A social blogging platform built with Flask.

## What This App Does

- Users can register, login, and post updates
- Follow other users to see their posts
- Search posts using Elasticsearch
- Translate posts to different languages (English, Spanish, Romanian)
- Send/receive private messages
- Real-time notifications
- Password reset via email

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: PostgreSQL (production), SQLite (local dev)
- **Search**: Elasticsearch via Bonsai
- **Translation**: Google Cloud Translate API
- **Email**: SendGrid API
- **Hosting**: Render.com
- **Other**: Flask-Login, Flask-WTF, Flask-Babel, Flask-Moment

## Local Development Setup

### Prerequisites
- Python 3.11+
- Git

### Installation

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/paperlight.git
cd paperlight
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` file:
```
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMINS=your-email@gmail.com
ELASTICSEARCH_URL=http://localhost:9200
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the app:
```bash
flask run
```

Visit http://localhost:5000

## Production Deployment (Render)

The app is deployed at: https://paperlight.onrender.com

### Environment Variables on Render:
- `DATABASE_URL` - PostgreSQL connection string (auto-set by Render)
- `SECRET_KEY` - Flask secret key
- `FLASK_APP` - Set to `paperlight.py`
- `SENDGRID_API_KEY` - SendGrid API key for emails
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD` - Email config
- `ADMINS` - Admin email for error notifications
- `ELASTICSEARCH_URL` - Bonsai Elasticsearch connection URL
- `GOOGLE_CREDENTIALS` - Full JSON content of Google Cloud credentials

### Build Command:
```bash
./build.sh
```

### Start Command:
```bash
gunicorn -b 0.0.0.0:$PORT "paperlight:app"
```

## Project Structure

```
paperlight/
├── app/
│   ├── auth/           # Authentication routes (login, register, password reset)
│   ├── errors/         # Error handlers (404, 500)
│   ├── main/           # Main app routes (index, profile, messages, etc)
│   ├── translations/   # Translation files for i18n
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, images
│   ├── __init__.py     # App factory
│   ├── models.py       # Database models (User, Post, Message, etc)
│   ├── email.py        # Email sending functions
│   ├── translate.py    # Google Translate integration
│   └── search.py       # Elasticsearch functions
├── migrations/         # Database migration files
├── venv/              # Virtual environment (not in git)
├── config.py          # App configuration
├── paperlight.py      # Main entry point
├── requirements.txt   # Python dependencies
├── build.sh          # Build script for Render
└── .env              # Local environment variables (not in git)
```

## Key Features Implementation

### Search (Elasticsearch)
- Posts are automatically indexed when created/updated
- Uses Bonsai free tier (125MB storage)
- Elasticsearch 7.17.9 client with monkey patch for Bonsai compatibility

### Translation (Google Cloud)
- Uses Google Cloud Translate API v2
- Credentials stored as JSON in environment variable
- AJAX requests for real-time translation

### Email (SendGrid)
- Password reset emails
- Error notifications to admins
- Uses SendGrid API (not SMTP) because Render free tier blocks SMTP

### Database
- PostgreSQL in production (via Render)
- SQLite for local development
- SQLAlchemy ORM with Flask-Migrate for migrations

## Chapters Completed from Tutorial

## Known Issues / Limitations

- Elasticsearch free tier only has 125MB storage
- SendGrid free tier limited to 100 emails/day
- Render free tier has cold starts (app sleeps after inactivity)
- Google Translate API is paid after free trial

## Troubleshooting

### "UnsupportedProductError" for Elasticsearch
- Bonsai uses OpenSearch, not standard Elasticsearch
- Solution: Monkey patch applied in `app/__init__.py`

### Database connection errors
- Make sure `DATABASE_URL` uses `postgresql+psycopg://` not `postgresql://`
- Check if `psycopg[binary]` is installed

## Contact

If you have questions, contact me at ttawela@gmail.com