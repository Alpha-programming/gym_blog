from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .import models

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        widgets = {
            'email':forms.EmailInput(
                attrs={'class': 'form-control'}
                )
            ,
            'first_name': forms.TextInput(
                attrs={'class':'form-control'}
                )
        }

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = models.WorkoutPlan
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = models.ExerciseLog
        fields = ['activity_type', 'distance_km', 'weight_kg', 'reps', 'duration_minutes']

        widgets = {
            'activity_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Running, Bench Press',
            }),
            'distance_km': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5.0',
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 60',
            }),
            'reps': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10',
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 30',
            }),
        }

        labels = {
            'activity_type': '🏋️ Activity Type',
            'distance_km': '📏 Distance (km)',
            'weight_kg': '🏋️‍♀️ Weight (kg)',
            'reps': '🔁 Repetitions',
            'duration_minutes': '⏱️ Duration (minutes)',
        }

        help_texts = {
            'activity_type': 'Describe the type of exercise (e.g. Squats, Treadmill).',
            'distance_km': 'Enter the distance covered (if applicable).',
            'weight_kg': 'Weight used in the exercise (if any).',
            'reps': 'Number of repetitions performed.',
            'duration_minutes': 'How long the activity lasted.',
        }

class FoodPlanForm(forms.ModelForm):
    class Meta:
        model = models.FoodPlan
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = models.FoodLog
        fields = ['food_name', 'calories', 'protein', 'fat', 'carbs']
        widgets = {
            'food_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Chicken Breast',
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 250',
            }),
            'protein': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 20',
            }),
            'fat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10',
            }),
            'carbs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 30',
            }),
        }
        labels = {
            'food_name': '🍎 Food Name',
            'calories': '🔥 Calories',
            'protein': '💪 Protein (g)',
            'fat': '🥑 Fat (g)',
            'carbs': '🍞 Carbohydrates (g)',
        }
        help_texts = {
            'food_name': 'Enter the name of the food item you ate.',
            'calories': 'Total calories in the food item.',
            'protein': 'Protein content in grams (important for muscle growth).',
            'fat': 'Fat content in grams. Healthy fats are essential!',
            'carbs': 'Carbs give you energy. Enter the amount in grams.',
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            })
        }
        labels = {
            'phone': 'Phone Number',
        }