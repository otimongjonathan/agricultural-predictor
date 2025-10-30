from app import create_app
from app.services.data_service import data_service
import os

app = create_app('production')

# Load data on startup
with app.app_context():
    data_service.load_data(app.config['DATA_FILES'])

if __name__ == '__main__':
    app.run()