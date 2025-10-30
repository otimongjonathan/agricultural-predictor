import numpy as np
from datetime import datetime, timedelta

class PredictionService:
    def __init__(self):
        # REALISTIC usage quantities per ACRE (in units)
        self.usage_quantities = {
            'seed_price': {
                'Maize': 25,      # 25kg per acre
                'Beans': 30,      # 30kg per acre  
                'Coffee': 15,     # 15kg per acre (seedlings)
                'Rice': 20,       # 20kg per acre
                'Cassava': 50,    # 50 stems per acre
                'Matooke': 20     # 20 suckers per acre
            },
            'fertilizer_price': {
                'Maize': 100,     # 100kg per acre
                'Beans': 80,      # 80kg per acre
                'Coffee': 150,    # 150kg per acre
                'Rice': 120,      # 120kg per acre
                'Cassava': 60,    # 60kg per acre
                'Matooke': 100    # 100kg per acre
            },
            'herbicide_price': {
                'Maize': 2,       # 2 litres per acre
                'Beans': 1.5,     # 1.5 litres per acre
                'Coffee': 3,      # 3 litres per acre
                'Rice': 2.5,      # 2.5 litres per acre
                'Cassava': 1,     # 1 litre per acre
                'Matooke': 2      # 2 litres per acre
            },
            'pesticide_price': {
                'Maize': 1.5,     # 1.5 litres per acre
                'Beans': 1,       # 1 litre per acre
                'Coffee': 2,      # 2 litres per acre
                'Rice': 1.8,      # 1.8 litres per acre
                'Cassava': 0.8,   # 0.8 litres per acre
                'Matooke': 1.5    # 1.5 litres per acre
            },
            'labor_cost': {
                'Maize': 15,      # 15 person-days per acre
                'Beans': 12,      # 12 person-days per acre
                'Coffee': 25,     # 25 person-days per acre
                'Rice': 20,       # 20 person-days per acre
                'Cassava': 10,    # 10 person-days per acre
                'Matooke': 18     # 18 person-days per acre
            }
        }
        
        # REALISTIC monthly inflation rates (much lower)
        self.inflation_rates = {
            'seed_price': 0.005,       # 0.5% monthly
            'fertilizer_price': 0.008,  # 0.8% monthly  
            'herbicide_price': 0.004,   # 0.4% monthly
            'pesticide_price': 0.006,   # 0.6% monthly
            'labor_cost': 0.010         # 1.0% monthly
        }
        
        # REALISTIC operational factors (transport, tools, etc.) - MUCH LOWER
        self.operational_factors = {
            'Central': 0.08,   # 8% - better infrastructure
            'Eastern': 0.10,   # 10% - moderate transport
            'Northern': 0.12,  # 12% - longer distances
            'Western': 0.09    # 9% - moderate transport
        }
        
        # Seasonal demand multipliers (by month 1-12)
        self.seasonal_multipliers = {
            'Maize': [1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.9, 1.0, 1.1, 1.1],
            'Beans': [1.0, 1.1, 1.2, 1.1, 1.0, 0.9, 0.8, 0.9, 1.0, 1.1, 1.2, 1.1],
            'Coffee': [1.0, 1.0, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 1.1, 1.2, 1.1, 1.0],
            'Rice': [1.2, 1.3, 1.4, 1.3, 1.2, 1.1, 1.0, 1.1, 1.2, 1.3, 1.2, 1.1],
            'Cassava': [1.0, 1.0, 1.0, 1.1, 1.1, 1.0, 1.0, 1.0, 1.0, 1.1, 1.1, 1.0],
            'Matooke': [1.1, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 1.0, 1.1, 1.2, 1.1, 1.0]
        }

    def predict_future_costs(self, region, district, crop, months_ahead=1, current_prices=None):
        # Default current prices (REALISTIC for smallholder farmers)
        if current_prices is None:
            current_prices = {
                'seed_price': 5000,        # UGX per kg
                'fertilizer_price': 3500,  # UGX per kg
                'herbicide_price': 12000,  # UGX per litre
                'pesticide_price': 11000,  # UGX per litre
                'labor_cost': 8000         # UGX per day
            }
        
        predictions = []
        
        # Calculate initial total cost PER ACRE
        initial_total_cost = 0
        for price_key, unit_price in current_prices.items():
            quantity = self.usage_quantities[price_key].get(crop, 1.0)
            initial_total_cost += unit_price * quantity
        
        # Add realistic operational costs
        operational_factor = self.operational_factors.get(region, 0.10)
        initial_total_cost_with_ops = initial_total_cost * (1 + operational_factor)
        
        for month_offset in range(1, months_ahead + 1):
            future_date = datetime.now() + timedelta(days=30 * month_offset)
            month = future_date.month
            
            base_costs = {}
            total_base_cost = 0
            
            # Calculate each input cost with inflation
            for price_key, unit_price in current_prices.items():
                inflation = self.inflation_rates.get(price_key, 0.01)
                projected_unit_price = unit_price * ((1 + inflation) ** month_offset)
                
                quantity = self.usage_quantities[price_key].get(crop, 1.0)
                actual_cost = projected_unit_price * quantity
                
                base_costs[price_key] = {
                    'unit_price': round(projected_unit_price, 2),
                    'quantity': quantity,
                    'total_cost': round(actual_cost, 2)
                }
                total_base_cost += actual_cost
            
            # Apply seasonal multiplier
            seasonal_pattern = self.seasonal_multipliers.get(crop, [1.0] * 12)
            seasonal_factor = seasonal_pattern[month - 1]
            seasonal_adjusted_cost = total_base_cost * seasonal_factor
            
            # Apply realistic operational costs
            operational_factor = self.operational_factors.get(region, 0.10)
            operational_costs = seasonal_adjusted_cost * operational_factor
            
            # Final predicted cost PER ACRE
            final_predicted_cost = seasonal_adjusted_cost + operational_costs
            
            # Small market variation (±2%)
            market_variation = 1.0 + (np.random.random() - 0.5) * 0.04
            final_predicted_cost *= market_variation
            
            # Calculate percentage change
            percentage_change = ((final_predicted_cost - initial_total_cost_with_ops) / initial_total_cost_with_ops) * 100
            
            predictions.append({
                'month': future_date.strftime("%B %Y"),
                'predicted_cost': round(final_predicted_cost, 2),
                'base_costs': base_costs,
                'total_base_cost': round(total_base_cost, 2),
                'seasonal_adjusted_cost': round(seasonal_adjusted_cost, 2),
                'operational_costs': round(operational_costs, 2),
                'percentage_change': round(percentage_change, 1),
                'calculation_details': {
                    'seasonal_factor': round(seasonal_factor, 3),
                    'operational_factor': operational_factor,
                    'market_variation': round(market_variation, 4)
                }
            })
        
        return predictions