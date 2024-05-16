from django import forms
from .models import Data
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class createData(forms.ModelForm):
    class Meta:
        model=Data
        fields=['song','artist','year','genre','rating']
    
        
    def clean_artist(self):
        artist=self.cleaned_data.get('artist')
        if not artist:
            raise forms.ValidationError("Required")
        return artist
    
    def clean_song(self):
        song=self.cleaned_data.get('song')
        if not song:
            raise forms.ValidationError("Required")
        return song