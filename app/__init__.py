import os
from flask import Flask, current_app

def create_app():
    app = Flask(__name__, static_folder='../public', template_folder='templates')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['GOOGLE_MODE'] = os.getenv('GOOGLE_MODE', 'TRUE') == 'TRUE'
    app.config['GOOGLE_SHEET_ID'] = os.getenv('GOOGLE_SHEET_ID')
    app.config['GOOGLE_CREDENTIALS_PATH'] = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials/google_credentials.json')

    # register blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.ticket_controller import ticket_bp
    from app.controllers.subscriber_controller import subscriber_bp
    from app.controllers.dashboard_controller import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ticket_bp, url_prefix='/tickets')
    app.register_blueprint(subscriber_bp, url_prefix='/subscribers')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # attach a placeholder sheets_service or db as needed
    if app.config['GOOGLE_MODE']:
        try:
            from app.services.google_sheets_service import GoogleSheetsService
            app.sheets_service = GoogleSheetsService()
        except Exception as e:
            app.logger.warning('GoogleSheetsService not initialized: ' + str(e))
    else:
        # initialize db singleton (lib.database.db)
        try:
            import lib.database as libdb
            app.db = libdb.db
        except Exception as e:
            app.logger.warning('Database not initialized: ' + str(e))

    return app