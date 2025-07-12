from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.api_client import api_client

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/')
def index():
    if 'logged_in' not in session:
        flash('Please log in to view notifications', 'error')
        return redirect(url_for('auth.login'))
    
    page = int(request.args.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    params = {
        'limit': per_page,
        'skip': skip,
        'unread_only': unread_only
    }
    
    # Get notifications
    notifications_response = api_client.get('/api/v1/notifications/', params=params)
    notifications = notifications_response.json() if notifications_response.status_code == 200 else []
    
    # Get notification stats
    stats_response = api_client.get('/api/v1/notifications/stats')
    stats = stats_response.json() if stats_response.status_code == 200 else {}
    
    return render_template('notifications/index.html', 
                         notifications=notifications,
                         stats=stats,
                         page=page,
                         unread_only=unread_only)

@notifications_bp.route('/mark-all-read', methods=['POST'])
def mark_all_read():
    if 'logged_in' not in session:
        flash('Please log in', 'error')
        return redirect(url_for('auth.login'))
    
    response = api_client.put('/api/v1/notifications/mark-all-read')
    
    if response.status_code == 200:
        flash('All notifications marked as read', 'success')
    else:
        flash('Error marking notifications as read', 'error')
    
    return redirect(url_for('notifications.index'))

@notifications_bp.route('/<notification_id>/read', methods=['POST'])
def mark_read(notification_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    response = api_client.put(f'/api/v1/notifications/{notification_id}/read')
    
    # Redirect to the question if available
    if response.status_code == 200:
        notification_data = response.json()
        if notification_data.get('question_id'):
            return redirect(url_for('questions.view', question_id=notification_data['question_id']))
    
    return redirect(url_for('notifications.index'))

