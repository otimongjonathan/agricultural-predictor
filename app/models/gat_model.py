import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv
import os

class HybridGATModel(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(HybridGATModel, self).__init__()
        self.gat1 = GATConv(in_channels, hidden_channels, heads=2, concat=True)
        self.gat2 = GATConv(hidden_channels * 2, hidden_channels, heads=1, concat=True)
        self.fc1 = nn.Linear(hidden_channels, hidden_channels // 2)
        self.fc2 = nn.Linear(hidden_channels // 2, out_channels)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x, edge_index):
        x = F.elu(self.gat1(x, edge_index))
        x = F.elu(self.gat2(x, edge_index))
        x = self.dropout(F.relu(self.fc1(x)))
        return self.fc2(x).squeeze()

# Global model instance
models = {}

def init_models(app):
    """Initialize models for the application"""
    try:
        device = torch.device(app.config['DEVICE'])
        
        # Initialize model architecture
        models['gat'] = HybridGATModel(
            in_channels=10,  # Adjust based on your feature count
            hidden_channels=64,
            out_channels=1
        ).to(device)
        
        # Load trained weights if available
        model_file = app.config['MODEL_PATH']
        if os.path.exists(model_file):
            try:
                checkpoint = torch.load(model_file, map_location=device)
                models['gat'].load_state_dict(checkpoint)
                models['gat'].eval()
                app.logger.info("Model loaded successfully")
            except Exception as e:
                app.logger.warning(f"Error loading model weights: {e}")
                app.logger.info("Using newly initialized model")
        else:
            app.logger.info("Model file not found. Using newly initialized model")
            
    except Exception as e:
        app.logger.error(f"Error initializing model: {e}")