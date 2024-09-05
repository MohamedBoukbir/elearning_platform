from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Use the CustomUser model you created earlier

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'country', 'gender', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class PerformanceForm(forms.Form):
    hours_studied = forms.FloatField(label='Hours Studied')
    previous_scores = forms.FloatField(label='Previous Scores')
    extracurricular = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')], label='Extracurricular Activities')
    sleep_hours = forms.FloatField(label='Sleep Hours')
    sample_papers = forms.IntegerField(label='Sample Question Papers Practiced')