"""
Plant Disease Prediction - Inference Module
This module provides functions for plant disease prediction from images.
"""
import os
import json
import pickle
import torch
from torch import nn
from PIL import Image
from typing import Tuple, List, Dict, Union, Any

# Default paths for model-related files
DEFAULT_MODEL_PATH = 'plant_disease/model.pth'
DEFAULT_ENCODER_PATH = 'plant_disease/label_encoder.pkl'
DEFAULT_TRANSFORM_PATH = 'plant_disease/inference_transform.pkl'
DEFAULT_CLASS_NAMES_PATH = 'plant_disease/class_names.json'


class PlantDiseaseModel(nn.Module):
    """Convolutional Neural Network for plant disease classification"""
    def __init__(self, num_classes, dropout_rate=0.5):
        super(PlantDiseaseModel, self).__init__()
        # Convolutional Block 1
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding="same"),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        # Convolutional Block 2
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding="same"),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        # Convolutional Block 3
        self.conv_block3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding="same"),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        # Convolutional Block 4
        self.conv_block4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding="same"),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        # Convolutional Block 5
        self.conv_block5 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding="same"),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        # Global Average Pooling
        self.global_avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        # Fully Connected Layers
        self.fc_block = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = self.conv_block4(x)
        x = self.conv_block5(x)
        x = self.global_avg_pool(x)
        x = self.fc_block(x)
        return x


# Cached model, transform and encoder for faster inference
_model_cache = {}
_transform_cache = {}
_label_encoder_cache = {}
_class_names_cache = {}


def load_model(model_path: str = DEFAULT_MODEL_PATH, 
               class_names_path: str = DEFAULT_CLASS_NAMES_PATH) -> Tuple[PlantDiseaseModel, torch.device]:
    """
    Load the plant disease prediction model
    
    Args:
        model_path: Path to the model file
        class_names_path: Path to the class names JSON file
        
    Returns:
        Tuple containing the loaded model and device
    """
    cache_key = model_path + class_names_path
    if cache_key in _model_cache:
        return _model_cache[cache_key]
    
    # Validate files existence
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(class_names_path):
        raise FileNotFoundError(f"Class names file not found: {class_names_path}")
    
    # Load class names
    if class_names_path not in _class_names_cache:
        with open(class_names_path, 'r') as f:
            _class_names_cache[class_names_path] = json.load(f)
    
    class_names = _class_names_cache[class_names_path]
    num_classes = len(class_names)
    
    # Initialize model
    model = PlantDiseaseModel(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    # Cache the model
    _model_cache[cache_key] = (model, device)
    
    return model, device


def load_transforms(transform_path: str = DEFAULT_TRANSFORM_PATH, 
                    label_encoder_path: str = DEFAULT_ENCODER_PATH) -> Tuple[Any, Any]:
    """
    Load transformation and label encoder
    
    Args:
        transform_path: Path to the transform pickle file
        label_encoder_path: Path to the label encoder pickle file
        
    Returns:
        Tuple containing transform and label encoder
    """
    # Load transform from cache if available
    if transform_path in _transform_cache:
        transform = _transform_cache[transform_path]
    else:
        if not os.path.exists(transform_path):
            raise FileNotFoundError(f"Transform file not found: {transform_path}")
        with open(transform_path, 'rb') as f:
            transform = pickle.load(f)
        _transform_cache[transform_path] = transform
    
    # Load label encoder from cache if available
    if label_encoder_path in _label_encoder_cache:
        label_encoder = _label_encoder_cache[label_encoder_path]
    else:
        if not os.path.exists(label_encoder_path):
            raise FileNotFoundError(f"Label encoder file not found: {label_encoder_path}")
        with open(label_encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        _label_encoder_cache[label_encoder_path] = label_encoder
    
    return transform, label_encoder


def predict_from_image(
    image_data: Union[str, bytes, Image.Image],
    model_path: str = DEFAULT_MODEL_PATH,
    label_encoder_path: str = DEFAULT_ENCODER_PATH,
    transform_path: str = DEFAULT_TRANSFORM_PATH,
    class_names_path: str = DEFAULT_CLASS_NAMES_PATH
) -> Dict[str, Any]:
    """
    Predict plant disease from an image
    
    Args:
        image_data: Either a file path (str), image bytes, or a PIL Image object
        model_path: Path to the trained model
        label_encoder_path: Path to the saved label encoder
        transform_path: Path to the saved transform
        class_names_path: Path to the class names JSON file
    
    Returns:
        Dictionary containing:
            - prediction: The top predicted disease class
            - confidence: Confidence score as percentage
            - top_predictions: List of top 3 predictions with their confidence scores
    """
    # Load model and required files
    model, device = load_model(model_path, class_names_path)
    transform, label_encoder = load_transforms(transform_path, label_encoder_path)
    
    # Process the image based on input type
    if isinstance(image_data, str):
        # It's a file path
        if not os.path.exists(image_data):
            raise FileNotFoundError(f"Image file not found: {image_data}")
        image = Image.open(image_data).convert('RGB')
    elif isinstance(image_data, bytes):
        # It's image bytes
        import io
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
    elif isinstance(image_data, Image.Image):
        # It's already a PIL Image
        image = image_data.convert('RGB')
    else:
        raise ValueError("Image data must be a file path, image bytes, or PIL Image object")
    
    # Preprocess image
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
    
    # Get top prediction
    top_prob, top_class = torch.max(probabilities, 0)
    predicted_class = label_encoder.inverse_transform([top_class.item()])[0]
    confidence = float(top_prob.item()) * 100
    
    # Get top-3 predictions with probabilities
    top3_probs, top3_indices = torch.topk(probabilities, 3)
    top3_classes = label_encoder.inverse_transform([idx.item() for idx in top3_indices])
    top3_results = [
        {"disease": class_name, "confidence": float(prob.item()) * 100} 
        for class_name, prob in zip(top3_classes, top3_probs)
    ]
    
    # Return structured results
    return {
        "prediction": predicted_class,
        "confidence": confidence,
        "top_predictions": top3_results
    }
