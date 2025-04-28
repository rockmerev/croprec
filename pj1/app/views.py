from django.shortcuts import render
from . import forms
import os
from django.conf import settings
from .forms import YieldPredictionForm
from app.utils.loaders import load_pickle
import numpy as np
def home_view(request):
    return render(request, 'home.html')

import pandas as pd
df = pd.read_csv(r"C:\Users\revan\Downloads\linux\mini-project\mp\crs\env\pj1\app\tnrg.csv")
df.columns = [
    "id", "serial_no", "district_name", "monsoon_recharge_rainfall",
    "monsoon_recharge_other_sources", "non_monsoon_recharge_rainfall",
    "non_monsoon_recharge_other_sources", "total_annual_recharge",
    "total_natural_discharges", "annual_extractable_gw_resource",
    "annual_extraction_irrigation", "annual_extraction_industrial",
    "annual_extraction_domestic", "total_annual_extraction",
    "gw_allocation_domestic_2025", "net_gw_availability_future",
    "gw_extraction_stage_percent"
]
def get_water_report(district):
    record = df[df["district_name"].str.lower() == district.lower()]
    
    if record.empty:
        return f"District '{district}' not found in dataset."
    
    record = record.iloc[0]
    monsoon_water = (
        record["monsoon_recharge_rainfall"] +
        record["monsoon_recharge_other_sources"]
    )
    non_monsoon_water = (
        record["non_monsoon_recharge_rainfall"] +
        record["non_monsoon_recharge_other_sources"]
    )
    total_used = (
        record["annual_extraction_irrigation"] +
        record["annual_extraction_industrial"] +
        record["annual_extraction_domestic"]
    )
    total_available = record["total_annual_recharge"] - record["total_natural_discharges"]-total_used
    return f"district: {district},monsoon_water: {monsoon_water},non_monsoon_water: {non_monsoon_water},total_water_used: {total_used},total_water_available: {total_available}"


def yield_prediction_view(request):
    prediction = None
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
            report = get_water_report(district)
            print(f"District: {district}, Crop: {crop}, Area: {area}, State: {state}")
            try:
                district_num = dist.transform([district])[0]
                crop_num = cp.transform([crop])[0]
            except ValueError as e:
                print(f"Error in encoding district or crop: {e}")
                return render(request, 'yld.html', {'form': form, 'prediction': "Invalid district or crop input."})
            input_data = [[district_num, crop_num]]
            print("Input Data for Yield Model:", input_data)
            predicted_yield_per_acre = yieldmodel.predict(input_data)[0]
            print("Predicted Yield per acre:", predicted_yield_per_acre)
            total_yield = predicted_yield_per_acre * area
            prediction = f"Estimated yield for {crop.title()} in {district}, {state} is {total_yield:.2f} tons/units average error is 900 kgs/units. /n  {report} for {district}"
    else:
        form = YieldPredictionForm()

    return render(request, 'yld.html', {'form': form, 'prediction': prediction})


from django.shortcuts import render
import pandas as pd
from . import forms
def crop_recommendation(request):
    result = None
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
            result = f"{crop_name} is the best crop to cultivate. Estimated yield for 1 acre: {predicted_yield_per_acre}tons."
    else:
        form = forms.CropForm()

    return render(request, 'form.html', {'form': form, 'result': result})
