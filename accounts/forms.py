from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Use the CustomUser model you created earlier

# Définition globale de GENDER_CHOICES
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

# Formulaire de création d'utilisateur personnalisé
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'country', 'gender', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # Mettre à jour les attributs des champs
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        
        # Utiliser les choix définis globalement pour le champ gender
        self.fields['gender'].choices = GENDER_CHOICES
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Gender'})

# Formulaire pour l'admin pour créer un étudiant
class AdminUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'country', 'gender']

    def __init__(self, *args, **kwargs):
        super(AdminUserCreationForm, self).__init__(*args, **kwargs)
        
        # Mettre à jour les attributs des champs
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})
        self.fields['gender'].choices = GENDER_CHOICES
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Gender'})

# Formulaire pour collecter les données de performance de l'étudiant
class PerformanceForm(forms.Form):
    hours_studied = forms.FloatField(label='Hours Studied', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    previous_scores = forms.FloatField(label='Previous Scores', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    extracurricular = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')], label='Extracurricular Activities', widget=forms.Select(attrs={'class': 'form-control'}))
    sleep_hours = forms.FloatField(label='Sleep Hours', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sample_papers = forms.IntegerField(label='Sample Question Papers Practiced', widget=forms.NumberInput(attrs={'class': 'form-control'}))
