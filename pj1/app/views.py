from django.shortcuts import render
from . import forms
import os
from django.conf import settings
from .forms import YieldPredictionForm
from app.utils.loaders import load_pickle
import numpy as np
def home_view(request):
    return render(request, 'home.html')


def yield_prediction_view(request):
    prediction = None

    # Update load_pickle paths to point to the models folder
    scaler1 = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'scaler1.pkl'))
    yieldmodel = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'yieldmodel.pkl'))
    dist = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'dist.pkl'))
    cp = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'label.pkl'))

    if request.method == "POST":
        form = YieldPredictionForm(request.POST)
        if form.is_valid():
            district = form.cleaned_data['district']
            area = form.cleaned_data['area']
            crop = form.cleaned_data['crop']
            state = form.cleaned_data['state']

            # Logging the form data
            print(f"District: {district}, Crop: {crop}, Area: {area}, State: {state}")

            # Convert district and crop names into numbers
            try:
                district_num = dist.transform([district])[0]
                crop_num = cp.transform([crop])[0]
            except ValueError as e:
                print(f"Error in encoding district or crop: {e}")
                return render(request, 'yld.html', {'form': form, 'prediction': "Invalid district or crop input."})
            input_data = [[district_num, crop_num]]
            print("Input Data for Yield Model:", input_data)
            predicted_yield_per_hectare = yieldmodel.predict(input_data)[0]
            print("Predicted Yield per Hectare:", predicted_yield_per_hectare)
            total_yield = predicted_yield_per_hectare * area
            prediction = f"Estimated yield for {crop.title()} in {district}, {state} is {total_yield:.2f} tons/units average error is 900 kgs/units."
    else:
        form = YieldPredictionForm()

    return render(request, 'yld.html', {'form': form, 'prediction': prediction})


from django.shortcuts import render
import pandas as pd
from . import forms
def crop_recommendation(request):
    result = None
    # Load the pre-trained models
    scaler = load_pickle('scaler.pkl')
    bestmodel = load_pickle('best_model.pkl')
    yieldmodel = load_pickle('yieldmodel.pkl')
    dist = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'dist.pkl'))
    cp = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'label.pkl'))

    if request.method == "POST":
        form = forms.CropForm(request.POST)
        if form.is_valid():
            nitrogen = form.cleaned_data['nitrogen']
            phosphorus = form.cleaned_data['phosphorus']
            potassium = form.cleaned_data['potassium']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']
            input_data = pd.DataFrame([{
                'N': nitrogen,
                'P': phosphorus,
                'K': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }])
            print(f"Input Data: {input_data}")
            scaled_data = scaler.transform(input_data)
            print(f"Scaled Data: {scaled_data}")
            predicted_class = bestmodel.predict(scaled_data)[0]
            print(f"Predicted Class (before mapping): {predicted_class}")
            crop_dict = {
                1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya",
                7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes",
                12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil", 16: "Blackgram",
                17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
            }

            crop_name = crop_dict.get(predicted_class + 1, "Unknown")
            
            try:
                crop_name=crop_name.lower()
                district='ARIYALUR'
                district_num = dist.transform([district])[0]
                crop_num = cp.transform([crop_name])[0]
                input_data = [[district_num, crop_num]]
                print("Input Data for Yield Model:", input_data)
                predicted_yield_per_acre = yieldmodel.predict(input_data)[0]
            except ValueError as e:
                print(f"Error in encoding district or crop: {e}")
                result = f"{crop_name} is the best crop to cultivate."
                return render(request, 'form.html', {'form': form, 'result': result})
            result = f"{crop_name} is the best crop to cultivate. Estimated yield for 1 hectare: {predicted_yield_per_acre}tons."
    else:
        form = forms.CropForm()

    return render(request, 'form.html', {'form': form, 'result': result})
