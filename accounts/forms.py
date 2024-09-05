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
