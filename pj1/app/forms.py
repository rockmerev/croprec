from django import forms

class CropForm(forms.Form):
    nitrogen = forms.FloatField(label="Nitrogen (N)", min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Nitrogen value'}))
    phosphorus = forms.FloatField(label="Phosphorus (P)", min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phosphorus value'}))
    potassium = forms.FloatField(label="Potassium (K)", min_value=0, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Potassium value'}))
    temperature = forms.FloatField(label="Temperature (°C)", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Temperature in °C'}))
    humidity = forms.FloatField(label="Humidity (%)", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Humidity percentage'}))
    ph = forms.FloatField(label="pH", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter pH value'}))
    rainfall = forms.FloatField(label="Rainfall (mm)", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Rainfall in mm'}))

"""class YieldPredictionForm(forms.Form):
    district = forms.CharField(
        label="District Name (UPPERCASE)", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control text-uppercase', 'oninput': 'this.value = this.value.toUpperCase();', 'required': True})
    )
    
    area = forms.FloatField(
        label="Built-up Area (in acres/hectares)", 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': True})
    )
    
    crop = forms.CharField(
        label="Crop Name", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )

    state = forms.CharField(
        label="State", 
        initial="Tamil Nadu", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True})
    )
"""