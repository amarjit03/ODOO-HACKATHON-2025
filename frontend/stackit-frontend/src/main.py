import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.main import main_bp
from src.routes.questions import questions_bp
from src.routes.api import api_bp
from src.routes.notifications import notifications_bp
from src.config import Config

app = Flask(__name__, 
           static_folder=os.path.join(os.path.dirname(__file__), 'static'),
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config.from_object(Config)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(questions_bp, url_prefix='/questions')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(notifications_bp, url_prefix='/notifications')

# uncomment if you need to use database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
