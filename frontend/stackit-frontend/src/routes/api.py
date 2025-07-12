from flask import Blueprint, request, jsonify, session
from src.api_client import api_client

api_bp = Blueprint('api', __name__)

# Voting endpoints
@api_bp.route('/votes/', methods=['POST'])
def vote_answer():
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to vote'}), 401
    
    data = request.get_json()
    if not data or 'answer_id' not in data or 'value' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    response = api_client.post('/api/v1/votes/', data)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        try:
            error_data = response.json()
            return jsonify({'error': error_data.get('detail', 'Voting failed')}), response.status_code
        except:
            return jsonify({'error': 'Voting failed'}), response.status_code

@api_bp.route('/votes/answer/<answer_id>', methods=['DELETE'])
def remove_vote(answer_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to remove vote'}), 401
    
    response = api_client.delete(f'/api/v1/votes/answer/{answer_id}')
    
    if response.status_code == 200:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to remove vote'}), response.status_code

# Answer acceptance
@api_bp.route('/answers/accept', methods=['POST'])
def accept_answer():
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to accept answers'}), 401
    
    data = request.get_json()
    if not data or 'answer_id' not in data:
        return jsonify({'error': 'Missing answer_id'}), 400
    
    response = api_client.post('/api/v1/answers/accept', data)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        try:
            error_data = response.json()
            return jsonify({'error': error_data.get('detail', 'Failed to accept answer')}), response.status_code
        except:
            return jsonify({'error': 'Failed to accept answer'}), response.status_code

# Tag endpoints
@api_bp.route('/tags/search')
def search_tags():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10)
    
    if not query:
        return jsonify([])
    
    response = api_client.get('/api/v1/tags/search', params={'q': query, 'limit': limit})
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify([])

@api_bp.route('/tags/', methods=['POST'])
def create_tag():
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to create tags'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing tag name'}), 400
    
    response = api_client.post('/api/v1/tags/', data)
    
    if response.status_code == 201:
        return jsonify(response.json())
    else:
        try:
            error_data = response.json()
            return jsonify({'error': error_data.get('detail', 'Failed to create tag')}), response.status_code
        except:
            return jsonify({'error': 'Failed to create tag'}), response.status_code

# Notification endpoints
@api_bp.route('/notifications/')
def get_notifications():
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to view notifications'}), 401
    
    params = {
        'limit': request.args.get('limit', 20),
        'skip': request.args.get('skip', 0),
        'unread_only': request.args.get('unread_only', 'false').lower() == 'true'
    }
    
    response = api_client.get('/api/v1/notifications/', params=params)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify([])

@api_bp.route('/notifications/unread-count')
def get_unread_count():
    if 'logged_in' not in session:
        return jsonify({'count': 0})
    
    response = api_client.get('/api/v1/notifications/unread-count')
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'count': 0})

@api_bp.route('/notifications/<notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in'}), 401
    
    response = api_client.put(f'/api/v1/notifications/{notification_id}/read')
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to mark notification as read'}), response.status_code

@api_bp.route('/notifications/mark-all-read', methods=['PUT'])
def mark_all_notifications_read():
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in'}), 401
    
    response = api_client.put('/api/v1/notifications/mark-all-read')
    
    if response.status_code == 200:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to mark all notifications as read'}), response.status_code

# Question and Answer proxy endpoints
@api_bp.route('/questions/user/<user_id>')
def get_user_questions(user_id):
    params = {
        'limit': request.args.get('limit', 20),
        'skip': request.args.get('skip', 0)
    }
    
    response = api_client.get(f'/api/v1/questions/user/{user_id}', params=params)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify([])

@api_bp.route('/answers/user/<user_id>')
def get_user_answers(user_id):
    params = {
        'limit': request.args.get('limit', 20),
        'skip': request.args.get('skip', 0)
    }
    
    response = api_client.get(f'/api/v1/answers/user/{user_id}', params=params)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify([])

