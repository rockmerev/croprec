import os
import pickle
from django.conf import settings

def load_pickle(filename):
    path = os.path.join(settings.BASE_DIR, 'app', 'models', filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in ml_models folder.")
    
    with open(path, 'rb') as f:
        return pickle.load(f)
