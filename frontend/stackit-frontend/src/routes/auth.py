from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.api_client import api_client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('auth/login.html')
        
        # Call backend API for login
        response = api_client.post('/api/v1/auth/login', {
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            data = response.json()
            session['access_token'] = data['access_token']
            session['logged_in'] = True
            
            # Get user info
            user_response = api_client.get('/api/v1/auth/me')
            if user_response.status_code == 200:
                user_data = user_response.json()
                session['user_id'] = user_data['id']
                session['username'] = user_data['username']
                session['user_role'] = user_data['role']
            
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')
        
        # Call backend API for registration
        response = api_client.post('/api/v1/auth/register', {
            'username': username,
            'email': email,
            'password': password
        })
        
        if response.status_code == 201:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            try:
                error_data = response.json()
                if 'detail' in error_data:
                    flash(f'Registration failed: {error_data["detail"]}', 'error')
                else:
                    flash('Registration failed. Please try again.', 'error')
            except:
                flash('Registration failed. Please try again.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
def profile():
    if 'logged_in' not in session:
        flash('Please log in to view your profile', 'error')
        return redirect(url_for('auth.login'))
    
    # Get user metrics
    user_response = api_client.get('/api/v1/metrics/my-metrics')
    user_metrics = user_response.json() if user_response.status_code == 200 else {}
    
    return render_template('auth/profile.html', user_metrics=user_metrics)

