from flask import Flask

def create_app(config_name='default'):
    app = Flask(__name__)
    app.secret_key = 'agricultural_predictor_secret_key'
    
    # Import and register blueprints
    from app.routes.views import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app