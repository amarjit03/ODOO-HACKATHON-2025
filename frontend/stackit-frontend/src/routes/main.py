from flask import Blueprint, render_template, request, session
from src.api_client import api_client

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get questions from API
    params = {
        'limit': 20,
        'skip': 0
    }
    
    # Add search and tag filters if provided
    search = request.args.get('search')
    tags = request.args.getlist('tags')
    
    if search:
        params['search'] = search
    if tags:
        params['tags'] = tags
    
    questions_response = api_client.get('/api/v1/questions/', params=params)
    questions = questions_response.json() if questions_response.status_code == 200 else []
    
    # Get popular tags
    tags_response = api_client.get('/api/v1/tags/popular', params={'limit': 10})
    popular_tags = tags_response.json() if tags_response.status_code == 200 else []
    
    # Get engagement stats
    stats_response = api_client.get('/api/v1/metrics/engagement')
    stats = stats_response.json() if stats_response.status_code == 200 else {}
    
    return render_template('index.html', 
                         questions=questions, 
                         popular_tags=popular_tags,
                         stats=stats,
                         search=search,
                         selected_tags=tags)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/leaderboard')
def leaderboard():
    # Get reputation leaderboard
    reputation_response = api_client.get('/api/v1/metrics/leaderboard/reputation', params={'limit': 20})
    reputation_leaders = reputation_response.json() if reputation_response.status_code == 200 else []
    
    # Get activity leaderboard
    activity_response = api_client.get('/api/v1/metrics/leaderboard/activity', params={'limit': 20})
    activity_leaders = activity_response.json() if activity_response.status_code == 200 else []
    
    return render_template('leaderboard.html', 
                         reputation_leaders=reputation_leaders,
                         activity_leaders=activity_leaders)

