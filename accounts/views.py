
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,AdminUserCreationForm


from .forms import PerformanceForm
from .models import CustomUser
from django.db.models import F
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import load_model
from django.conf import settings
import os

from transformers import GPT2LMHeadModel, GPT2Tokenizer

from datetime import timedelta
from django.utils import timezone


from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return user.is_authenticated and user.role == 'admin'

def student_check(user):
    return user.is_authenticated and user.role == 'student'



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
            # Redirection en fonction du rôle
            if user.role == 'admin':
                return redirect('dashboardadmin')
            elif user.role == 'student':
                if user.score is not None:
                    return redirect('dashboard')
                else:
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

# @login_required
# def dashboard(request):
#     user = request.user
#     current_time = timezone.now()
#     show_questionnaire_button = True

#     # Check if a week has passed since the last submission
#     if user.last_submission_date:
#         time_since_last_submission = current_time - user.last_submission_date
#         if time_since_last_submission < timedelta(weeks=1):
#             show_questionnaire_button = False
#     return render(request, 'accounts/dashboard.html', {'show_questionnaire_button': show_questionnaire_button})




@user_passes_test(admin_check, login_url='access_denied')
def dashboardadmin(request):
    return render(request, 'admin/dashboard.html')





# def access_denied(request):
#     return render(request, 'accounts/forbidden.html', status=403)





# Construire le chemin absolu vers les fichiers de modèle
MODEL_FILE_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'student_performance_model.h5')
SCALER_FILE_PATH = os.path.join(settings.BASE_DIR, 'model_files', 'scaler.pkl')

# Charger le modèle et le scaler
model = load_model(MODEL_FILE_PATH)
scaler = joblib.load(SCALER_FILE_PATH)
@user_passes_test(student_check, login_url='access_denied')
def calculate_score(request):
    user = request.user
    current_time = timezone.now()
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
            user.last_submission_date = current_time
            user.save()

            return redirect('dashboard')  # Rediriger vers le tableau de bord après la mise à jour

    else:
        form = PerformanceForm()
    

    return render(request, 'calculate_score.html', {'form': form})





@user_passes_test(student_check, login_url='access_denied')
def dashboard(request):
    user = request.user
    current_time = timezone.now()
    show_questionnaire_button = True
    response = None  # Variable pour stocker la réponse générée par GPT-2

    # Check if a week has passed since the last submission
    if user.last_submission_date:
        time_since_last_submission = current_time - user.last_submission_date
        if time_since_last_submission < timedelta(weeks=1):
            show_questionnaire_button = False

    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            print("ok score")
            print(user.score/5)
            response = generate_answer(question, user.score/5)  # Passer le score de l'utilisateur à la fonction de génération

    # Rendre la page dashboard avec la réponse si elle existe
    return render(request, 'accounts/dashboard.html', {
        'show_questionnaire_button': show_questionnaire_button,
        'response': response  # Passer la réponse au template
    })



# Charger le modèle et le tokenizer GPT-2 fine-tuné
model_path = r"C:/Users/Mohamed/projetgpt/gpt2-finetuned-squad"
modelGpt = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# def generate_answer(question):
#     inputs = tokenizer.encode(f"Question: {question}", return_tensors='pt')
#     outputs = model.generate(inputs, max_length=100)
#     answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return answer



def generate_answer(question, score):
    # Ajuster le prompt en fonction du score
    if score < 10:
        prompt = f"Question: {question}\nExplication détaillée :"
    elif 10 <= score < 12:
        prompt = f"Question: {question}\nExplication :"
    elif 12 <= score < 14:
        prompt = f"Question: {question}\nRéponse simple :"
    elif 14 <= score < 16:
        prompt = f"Question: {question}\nRéponse concise :"
    else:
        prompt = f"Question: {question}\nRésumé :"

    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = modelGpt.generate(inputs, max_length=150, min_length=40, length_penalty=1.2, num_beams=5, early_stopping=True, temperature=1.2, top_p=0.9, do_sample=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer





# def generate_answer(question, user_score):
#     # Personnaliser la question en fonction du score de l'utilisateur
#     if user_score is not None:
#         personalized_question = f"Question: {question} (Score: {user_score})"
#     else:
#         personalized_question = f"Question: {question}"

#     # Encoder la question avec le tokenizer GPT-2
#     inputs = tokenizer.encode(personalized_question, return_tensors='pt')
    
#     # Générer la réponse avec le modèle GPT-2
#     outputs = model.generate(inputs, max_length=100)
#     answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     return answer


@login_required
def access_denied(request):
    if request.user.role == 'student':
        return render(request, 'accounts/access_denied.html', {
            'redirect_url': 'dashboard'  # URL pour le tableau de bord des étudiants
        })
    elif request.user.role == 'admin':
        return render(request, 'accounts/access_denied.html', {
            'redirect_url': 'dashboardadmin'  # URL pour le tableau de bord des administrateurs
        })
    else:
        return render(request, 'accounts/access_denied.html', {
            'redirect_url': 'welcome'  # URL pour une page par défaut si le rôle n'est pas reconnu
        })

def logout(request):
    auth_logout(request)
    return redirect('login')








#  **********************************
#             Admin start 
#         ***********************************

# Afficher la liste des étudiants
@login_required
def student_list(request):
    students = CustomUser.objects.filter(role='student')
    return render(request, 'admin/all-students.html', {'students': students})

@login_required
def create_student(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        
        if form.is_valid():
            print("post create")
            user = form.save(commit=False)

            # Générer un mot de passe automatique : first_name + last_name
            generated_password = form.cleaned_data['first_name'] + form.cleaned_data['last_name']
            user.set_password(generated_password)  # Utiliser set_password pour sécuriser le mot de passe

            user.save()  # Sauvegarder l'utilisateur avec le mot de passe sécurisé
            return redirect('student_list')  # Redirection vers la liste des étudiants après la création
        else:
            # Imprimer les erreurs dans la console
            print(form.errors)  # Voir les erreurs de validation
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'admin/add-student.html', {'form': form})



@login_required
def update_student(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)  # Obtenir l'étudiant en fonction de l'ID (pk)
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST, instance=student)  # Charger l'étudiant existant dans le formulaire
        if form.is_valid():
            form.save()  # Sauvegarder les modifications
            return redirect('student_list')  # Rediriger vers la liste des étudiants après la mise à jour
    else:
        form = AdminUserCreationForm(instance=student)  # Pré-remplir le formulaire avec les données de l'étudiant
    
    return render(request, 'admin/edit-student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')  # Redirige vers la liste des étudiants après suppression
    return redirect('student_list')  # Redirige vers la liste des étudiants en cas de requête non-POST

#  **********************************
#             Admin end  
#         ***********************************
