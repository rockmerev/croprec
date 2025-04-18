from django.shortcuts import render
from . import forms
import pickle
import os
from django.conf import settings
from sklearn.preprocessing import StandardScaler
from .forms import YieldPredictionForm
from app.utils.loaders import load_pickle

def home_view(request):
    return render(request, 'home.html')


def yield_prediction_view(request):
    prediction = None
    # scaler1 = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'scaler1.pkl'))
    # yieldmodel = load_pickle(os.path.join(settings.BASE_DIR, 'app', 'models', 'yieldmodel.pkl'))
    scaler1 = load_pickle('scaler1.pkl')
    yieldmodel = load_pickle('yieldmodel.pkl')
    cp=load_pickle('label.pkl')
    dp=load_pickle('dist.pkl')
    # Debugging step: check the type of loaded model
    print("Type of yieldmodel:", type(yieldmodel))
    
    if request.method == "POST":
        form = YieldPredictionForm(request.POST)
        if form.is_valid():
            district = form.cleaned_data['district']
            area = form.cleaned_data['area']
            crop = form.cleaned_data['crop']
            state = form.cleaned_data['state']

            district_c = {'ARIYALUR':1,'COIMBATORE':2,'CUDDALORE':3,'DHARMAPURI':4,'DINDIGUL':5,'ERODE':6,'KANCHIPURAM':7,'KANNIYAKUMARI':8,'KARUR':9,'KRISHNAGIRI':10,'MADURAI':11,'NAGAPATTINAM':12,'NAMAKKAL':13,'PERAMBALUR':14,'PUDUKKOTTAI':15,'RAMANATHAPURAM':16,'SALEM':17,'SIVAGANGA':18,'THANJAVUR':19,'THE NILGIRIS':20,'THENI':21,'THIRUVALLUR':22,'THIRUVARUR':23,'TIRUCHIRAPPALLI':24,'TIRUNELVELI':25,'TUTICORIN':28,'VELLORE':29,'VILLUPURAM':30,'VIRUDHUNAGAR':31}
            cropd = {'rice':1,'maize':2,'jute':3,'cotton':4,'coconut':5,'papaya':6,'orange':7,'apple':8,'muskmelon':9,'watermelon':10,'grapes':11,'mango':12,'banana':13,'pomegranate':14,'lentil':15,'blackgram':16,'mungbean':17,'mothbeans':18,'pigeonpeas':19,'kidneybeans':20,'chickpea':21,'coffee':22,'smallmillets':23,'arhar/tur':24,'bajra':25,'cashewnut':26,'castorseed':27,'coriander':28,'cotton(lint)':29,'drychillies':30,'groundnut':31,'jowar':32,'moong(greengram)':33,'onion':34,'ragi':35,'sesamum':36,'sugarcane':37,'sunflower':38,'sweetpotato':39,'tapioca':40,'turmeric':41,'urad':42,'horse-gram':43,'tobacco':44,'blackpepper':45,'cardamom':46,'gram':47,'pulsestotal':48,'totalfoodgrain':49,'wheat':50,'sannhamp':51,'korra':52,'samai':53,'guarseed':54,'othercereals&millets':55,'otherkharifpulses':56,'rapeseed&mustard':57,'varagu':58,'ashgourd':59,'beans&mutter(vegetable)':60,'beetroot':61,'bhindi':62,'bittergourd':63,'bottlegourd':64,'brinjal':65,'cauliflower':66,'citrusfruit':67,'cucumber':68,'drumstick':69,'garlic':70,'jackfruit':71,'lab-lab':72,'othercitrusfruit':73,'otherfreshfruits':74,'othervegetables':75,'pomefruit':76,'pomegranate':77,'redish':78,'ribedguard':79,'snakguard':80,'tomato':81,'yam':82,'cabbage':83,'pumpkin':84,'dryginger':85,'arecanut':86,'potato':87,'carrot':88,'pineapple':89,'mesta':90,'peach':91,'pear':92,'plums':93,'turnip':94,'litchi':95,'ber':96}

            district_num = district_c.get(district, 0)
            crop_num = cropd.get(crop, 0)
            cn=cp.transform([crop])[0]
            dn=dp.transform([district])[0]
            # Feature vector
            input_data = [[dn, cn]]
            # scaled_data = scaler1.transform(input_data)

            # Debugging step: print the shape of scaled data
            
            # ✅ Use predict() for prediction
            predicted_yield_per_hectare = yieldmodel.predict(input_data)
            
            # Debugging step: print the prediction
            print("Predicted yield per hectare:", predicted_yield_per_hectare)

            total_yield = predicted_yield_per_hectare * area

            prediction = f"Estimated yield for {crop} in {district} is {total_yield} tons."

    else:
        form = YieldPredictionForm()

    return render(request, 'yld.html', {'form': form, 'prediction': prediction})


def crop_recommendation(request):
    result=None
    scaler = load_pickle('scaler.pkl')
    bestmodel = load_pickle('best_model.pkl')
    yieldmodel = load_pickle('yieldmodel.pkl')
    cp=load_pickle('label.pkl')
    dp=load_pickle('dist.pkl')
    # Debugging step: check the type of loaded models
    print("Type of bestmodel:", type(bestmodel))
    print("Type of yieldmodel:", type(yieldmodel))

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
            
            input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
            scaled_data = scaler.transform(input_data)
            
            # Debugging step: print the shape of scaled data
            print("Shape of scaled data for crop recommendation:", scaled_data.shape)

            prediction = bestmodel.predict(scaled_data)[0]

            crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                         8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                         14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                         19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

            crop = crop_dict.get(prediction+1, "Unknown")
            
            

            # Debugging step: check raw model prediction
            prediction_raw = bestmodel.predict(scaled_data)
            print("Raw model prediction:", prediction_raw)
            district='ARIYALUR'
            cn=cp.transform([crop.capitalize()])[0]
            dn=dp.transform([district])[0]
            input_data = [[dn, cn]]
            predicted_yield_per_acre = yieldmodel.predict(input_data)
            area = 1
            district = 'ARIYALUR'
            district_c = {'ARIYALUR':1, 'COIMBATORE':2, 'CUDDALORE':3, 'DHARMAPURI':4, 'DINDIGUL':5, 'ERODE':6, 'KANCHIPURAM':7, 'KANNIYAKUMARI':8, 'KARUR':9, 'KRISHNAGIRI':10, 'MADURAI':11, 'NAGAPATTINAM':12, 'NAMAKKAL':13, 'PERAMBALUR':14, 'PUDUKKOTTAI':15, 'RAMANATHAPURAM':16, 'SALEM':17, 'SIVAGANGA':18, 'THANJAVUR':19, 'THE NILGIRIS':20, 'THENI':21, 'THIRUVALLUR':22, 'THIRUVARUR':23, 'TIRUCHIRAPPALLI':24, 'TIRUNELVELI':25, 'TUTICORIN':28, 'VELLORE':29, 'VILLUPURAM':30, 'VIRUDHUNAGAR':31}
            result = f"{crop} is the best crop to be cultivated right there and yield for 1 acre is  s{predicted_yield_per_acre} in ariyalur district. you can check yiled per acre also..."

    else:
        form = forms.CropForm()

    return render(request, 'form.html', {'form': form, 'result': result})
