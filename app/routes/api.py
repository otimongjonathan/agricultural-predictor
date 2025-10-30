from flask import Blueprint, request, jsonify
from app.services.prediction_service import PredictionService

api_bp = Blueprint('api', __name__)
prediction_service = PredictionService()

@api_bp.route('/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json()
        
        region = data.get('region')
        district = data.get('district')
        crop = data.get('crop')
        months_ahead = data.get('months_ahead', 1)
        
        current_prices = data.get('current_prices', {
            'seed_price': 5000, 'fertilizer_price': 4000, 'herbicide_price': 15000,
            'pesticide_price': 14000, 'labor_cost': 10000
        })
        
        predictions = prediction_service.predict_future_costs(
            region, district, crop, months_ahead, current_prices
        )
        
        return jsonify({
            'status': 'success',
            'region': region,
            'district': district,
            'crop': crop,
            'predictions': predictions
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Agricultural Cost Predictor'})

@api_bp.route('/regions', methods=['GET'])
def get_regions():
    regions = ['Central', 'Eastern', 'Northern', 'Western']
    return jsonify({'regions': regions})

@api_bp.route('/districts/<region>', methods=['GET'])
def get_districts_api(region):
    districts_map = {
        'Central': ['Kampala', 'Wakiso', 'Mukono', 'Masaka'],
        'Eastern': ['Jinja', 'Iganga', 'Mbale', 'Soroti'],
        'Northern': ['Gulu', 'Lira', 'Arua', 'Kitgum'],
        'Western': ['Mbarara', 'Fort Portal', 'Kabale', 'Hoima']
    }
    districts = districts_map.get(region, [])
    return jsonify({'districts': districts})

@api_bp.route('/crops/<district>', methods=['GET'])
def get_crops_api(district):
    crops = ['Maize', 'Beans', 'Coffee', 'Rice', 'Cassava', 'Matooke']
    return jsonify({'crops': crops})