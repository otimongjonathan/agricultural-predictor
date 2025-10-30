from flask import Blueprint, render_template, request, jsonify
from app.services.prediction_service import PredictionService
import os

# Define the blueprint FIRST
main_bp = Blueprint('main', __name__)
prediction_service = PredictionService()

@main_bp.route('/')
def index():
    regions = ['Central', 'Eastern', 'Northern', 'Western']
    districts = ['Kampala', 'Wakiso', 'Jinja', 'Mbale', 'Gulu', 'Lira', 'Luweero']
    crops = ['Maize', 'Beans', 'Coffee', 'Rice', 'Cassava', 'Matooke']
    
    return render_template('index.html', 
                         regions=regions,
                         districts=districts,
                         crops=crops)

@main_bp.route('/predict', methods=['POST'])
def predict():
    try:
        region = request.form['region']
        district = request.form['district']
        crop = request.form['crop']
        months_ahead = int(request.form['months_ahead'])
        
        # Use realistic default prices (no user input needed)
        current_prices = {
            'seed_price': 5000,        # UGX per kg
            'fertilizer_price': 3500,  # UGX per kg
            'herbicide_price': 12000,  # UGX per litre
            'pesticide_price': 11000,  # UGX per litre
            'labor_cost': 8000         # UGX per day
        }
        
        predictions = prediction_service.predict_future_costs(
            region, district, crop, months_ahead, current_prices
        )
        
        return render_template('results.html',
                            region=region,
                            district=district, 
                            crop=crop,
                            predictions=predictions,
                            current_prices=current_prices)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

# Add other routes if needed
@main_bp.route('/get_districts/<region>')
def get_districts(region):
    districts_map = {
        'Central': ['Kampala', 'Wakiso', 'Mukono', 'Masaka'],
        'Eastern': ['Jinja', 'Iganga', 'Mbale', 'Soroti'],
        'Northern': ['Gulu', 'Lira', 'Arua', 'Kitgum'],
        'Western': ['Mbarara', 'Fort Portal', 'Kabale', 'Hoima']
    }
    districts = districts_map.get(region, [])
    return jsonify(districts)

@main_bp.route('/get_crops/<region>/<district>')
def get_crops(region, district):
    crops = ['Maize', 'Beans', 'Coffee', 'Rice', 'Cassava', 'Matooke']
    return jsonify(crops)