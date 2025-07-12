# StackIt - Q&A Forum Frontend

A complete frontend application for the StackIt Q&A forum platform built with Flask, connecting to the backend API at `http://3.82.218.27`.

## Features

- **User Authentication**: Register, login, logout, and user profiles
- **Question Management**: Ask, edit, view, and search questions
- **Rich Text Editor**: Quill.js-powered editor with formatting, links, images, and code blocks
- **Answer System**: Post answers, accept answers, and vote on content
- **Tagging System**: Tag-based categorization and filtering
- **Voting System**: Upvote/downvote answers with reputation scoring
- **Notification System**: Real-time notifications for answers, votes, and mentions
- **Leaderboard**: Reputation and activity-based rankings
- **Responsive Design**: Bootstrap-based UI that works on desktop and mobile

## Project Structure

```
stackit-frontend/
├── src/
│   ├── routes/          # Flask blueprint files
│   │   ├── auth.py      # Authentication routes
│   │   ├── main.py      # Main application routes
│   │   ├── questions.py # Question management routes
│   │   ├── api.py       # API proxy routes
│   │   └── notifications.py # Notification routes
│   ├── templates/       # Jinja2 HTML templates
│   │   ├── auth/        # Authentication templates
│   │   ├── questions/   # Question-related templates
│   │   └── notifications/ # Notification templates
│   ├── static/          # Static files
│   ├── models/          # Database models
│   ├── main.py          # Main Flask application
│   ├── config.py        # Configuration settings
│   └── api_client.py    # Backend API client
├── venv/                # Virtual environment (excluded from zip)
└── requirements.txt     # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Extract the project**:
   ```bash
   unzip stackit-frontend.zip
   cd stackit-frontend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key-here
   API_BASE_URL=http://3.82.218.27
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Configuration

The application can be configured through environment variables or by modifying `src/config.py`:

- `SECRET_KEY`: Flask secret key for sessions
- `API_BASE_URL`: Backend API base URL (default: http://3.82.218.27)

## API Integration

The frontend connects to the StackIt backend API with the following endpoints:

- **Authentication**: `/api/v1/auth/*`
- **Questions**: `/api/v1/questions/*`
- **Answers**: `/api/v1/answers/*`
- **Voting**: `/api/v1/votes/*`
- **Tags**: `/api/v1/tags/*`
- **Notifications**: `/api/v1/notifications/*`
- **Metrics**: `/api/v1/metrics/*`

## Key Features Implementation

### Rich Text Editor
- Uses Quill.js for WYSIWYG editing
- Supports formatting, lists, links, images, and code blocks
- Integrated in question asking and answer posting

### Voting System
- AJAX-based voting without page refresh
- Real-time vote count updates
- User vote state tracking

### Notification System
- Real-time notification polling
- Dropdown notification preview
- Full notification management page

### Responsive Design
- Bootstrap 5 for responsive layout
- Mobile-friendly navigation
- Touch-friendly interface elements

## Development

### Adding New Features
1. Create new routes in appropriate blueprint files
2. Add corresponding templates in the templates directory
3. Update navigation in `base.html` if needed
4. Test functionality locally before deployment

### Customization
- Modify templates in `src/templates/` for UI changes
- Update styles in `base.html` or add separate CSS files
- Extend API client in `src/api_client.py` for new endpoints

## Deployment

### Production Deployment
For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. **Set environment variables**:
   ```bash
   export SECRET_KEY="your-production-secret-key"
   export API_BASE_URL="https://your-api-domain.com"
   ```

3. **Use a reverse proxy** (e.g., Nginx) for static files and SSL termination

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 5000
CMD ["python", "src/main.py"]
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**:
   - Verify the backend API is running at the configured URL
   - Check network connectivity to the API endpoint

2. **Template Not Found Errors**:
   - Ensure all template files are in the correct directory structure
   - Check that blueprint registrations include correct URL prefixes

3. **Static Files Not Loading**:
   - Verify static folder configuration in `main.py`
   - Check file permissions and paths

### Debug Mode
The application runs in debug mode by default for development. For production, set:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

## Contributing

1. Follow the existing code structure and naming conventions
2. Add appropriate error handling and validation
3. Test all functionality before submitting changes
4. Update documentation for new features

## License

This project is part of the StackIt Q&A platform implementation.

