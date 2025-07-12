from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.api_client import api_client

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/ask', methods=['GET', 'POST'])
def ask():
    if 'logged_in' not in session:
        flash('Please log in to ask a question', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.getlist('tags')
        
        if not title or not description:
            flash('Title and description are required', 'error')
            return render_template('questions/ask.html')
        
        # Call backend API to create question
        response = api_client.post('/api/v1/questions/', {
            'title': title,
            'description': description,
            'tags': tags
        })
        
        if response.status_code == 201:
            question_data = response.json()
            flash('Question posted successfully!', 'success')
            return redirect(url_for('questions.view', question_id=question_data['id']))
        else:
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    flash(f'Error posting question: {error_data["detail"]}', 'error')
                else:
                    flash('Error posting question. Please try again.', 'error')
            except:
                flash('Error posting question. Please try again.', 'error')
    
    # Get all tags for the tag selector
    tags_response = api_client.get('/api/v1/tags/', params={'limit': 100})
    all_tags = tags_response.json() if tags_response.status_code == 200 else []
    
    return render_template('questions/ask.html', all_tags=all_tags)

@questions_bp.route('/<question_id>')
def view(question_id):
    # Get question details
    question_response = api_client.get(f'/api/v1/questions/{question_id}')
    if question_response.status_code != 200:
        flash('Question not found', 'error')
        return redirect(url_for('main.index'))
    
    question = question_response.json()
    
    # Get answers for this question
    answers_response = api_client.get(f'/api/v1/answers/question/{question_id}')
    answers = answers_response.json() if answers_response.status_code == 200 else []
    
    # Get vote stats for each answer if user is logged in
    if 'logged_in' in session:
        for answer in answers:
            vote_response = api_client.get(f'/api/v1/votes/answer/{answer["id"]}/stats')
            if vote_response.status_code == 200:
                answer['vote_stats'] = vote_response.json()
            
            # Get user's vote for this answer
            my_vote_response = api_client.get(f'/api/v1/votes/answer/{answer["id"]}/my-vote')
            if my_vote_response.status_code == 200:
                answer['my_vote'] = my_vote_response.json()
    
    return render_template('questions/view.html', question=question, answers=answers)

@questions_bp.route('/<question_id>/answer', methods=['POST'])
def post_answer(question_id):
    if 'logged_in' not in session:
        return jsonify({'error': 'Please log in to post an answer'}), 401
    
    description = request.form.get('description')
    if not description:
        return jsonify({'error': 'Answer description is required'}), 400
    
    # Call backend API to create answer
    response = api_client.post('/api/v1/answers/', {
        'description': description,
        'question_id': question_id
    })
    
    if response.status_code == 201:
        flash('Answer posted successfully!', 'success')
        return redirect(url_for('questions.view', question_id=question_id))
    else:
        flash('Error posting answer. Please try again.', 'error')
        return redirect(url_for('questions.view', question_id=question_id))

@questions_bp.route('/edit/<question_id>', methods=['GET', 'POST'])
def edit(question_id):
    if 'logged_in' not in session:
        flash('Please log in to edit questions', 'error')
        return redirect(url_for('auth.login'))
    
    # Get question details
    question_response = api_client.get(f'/api/v1/questions/{question_id}')
    if question_response.status_code != 200:
        flash('Question not found', 'error')
        return redirect(url_for('main.index'))
    
    question = question_response.json()
    
    # Check if user owns this question
    if question['user_id'] != session['user_id']:
        flash('You can only edit your own questions', 'error')
        return redirect(url_for('questions.view', question_id=question_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.getlist('tags')
        
        update_data = {}
        if title:
            update_data['title'] = title
        if description:
            update_data['description'] = description
        if tags:
            update_data['tags'] = tags
        
        # Call backend API to update question
        response = api_client.put(f'/api/v1/questions/{question_id}', update_data)
        
        if response.status_code == 200:
            flash('Question updated successfully!', 'success')
            return redirect(url_for('questions.view', question_id=question_id))
        else:
            flash('Error updating question. Please try again.', 'error')
    
    # Get all tags for the tag selector
    tags_response = api_client.get('/api/v1/tags/', params={'limit': 100})
    all_tags = tags_response.json() if tags_response.status_code == 200 else []
    
    return render_template('questions/edit.html', question=question, all_tags=all_tags)

@questions_bp.route('/search')
def search():
    query = request.args.get('q', '')
    tags = request.args.getlist('tags')
    page = int(request.args.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page
    
    params = {
        'limit': per_page,
        'skip': skip
    }
    
    if query:
        params['search'] = query
    if tags:
        params['tags'] = tags
    
    # Get questions from API
    questions_response = api_client.get('/api/v1/questions/', params=params)
    questions = questions_response.json() if questions_response.status_code == 200 else []
    
    # Get popular tags
    tags_response = api_client.get('/api/v1/tags/popular', params={'limit': 20})
    popular_tags = tags_response.json() if tags_response.status_code == 200 else []
    
    return render_template('questions/search.html', 
                         questions=questions, 
                         popular_tags=popular_tags,
                         query=query,
                         selected_tags=tags,
                         page=page)

