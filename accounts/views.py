from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


from .forms import PerformanceForm
from .models import CustomUser
from django.db.models import F
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import load_model
from django.conf import settings
import os

def welcome(request):
    print("welcom ok")
    return render(request, 'accounts/welcome.html')

def login_view(request):
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
             # Vérifier le score de l'utilisateur
            if user.score is not None:
                # Si le score est présent, rediriger vers le dashboard
                return redirect('dashboard')
            else:
                # Sinon, rediriger vers une vue de calcul du score
                return redirect('calculate_score')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')
    # print("ok ok")
    # return render(request, 'login.html')

# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/register.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def logout(request):
    auth_logout(request)
    return redirect('login')


# Construire le chemin absolu vers les fichiers de modèle
MODEL_FILE_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'student_performance_model.h5')
SCALER_FILE_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'scaler.pkl')

# Charger le modèle et le scaler
model = load_model(MODEL_FILE_PATH)
scaler = joblib.load(SCALER_FILE_PATH)
@login_required
def calculate_score(request):
    user = request.user

    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            hours_studied = form.cleaned_data['hours_studied']
            previous_scores = form.cleaned_data['previous_scores']
            extracurricular = form.cleaned_data['extracurricular']
            sleep_hours = form.cleaned_data['sleep_hours']
            sample_papers = form.cleaned_data['sample_papers']

            features = np.array([[hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers]])
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)
            predicted_performance = float(prediction[0][0])

            # Mettre à jour le score de l'utilisateur
            user.score = predicted_performance
            user.save()

            return redirect('dashboard')  # Rediriger vers le tableau de bord après la mise à jour

    else:
        form = PerformanceForm()

    return render(request, 'calculate_score.html', {'form': form})