from django import forms
from .models import Recipe, Ingredient, Step, IngreadientMeasure, CustomUser, Category
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'prep_time', 'prep_time_unit',
            'cook_time', 'cook_time_unit',
            'spice_level',
            'category',
            'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Short description about the recipe'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'e.g., 10'
            }),
            'prep_time_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'e.g., 30'
            }),
            'cook_time_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'spice_level': forms.Select(attrs={
                'class': 'form-select',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use empty_label to define a custom placeholder for ModelChoiceField
        self.fields['category'].empty_label = '— Select a category —'
        self.fields['category'].widget.attrs.update({'required': True})
        self.fields['spice_level'].empty_label = '— Select Spice Level —'
        self.fields['spice_level'].widget.attrs.update({'required': True})
   
class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'measure']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'List ingredients'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 kg'}),
            'measure': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use empty_label to define a custom placeholder for ModelChoiceField
        self.fields['measure'].empty_label = '— Select Measure —'
        self.fields['measure'].widget.attrs.update({'required': True})

class StepsForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['step_number', 'step']
        widgets = {
            'step_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 or 2 etc...'}),
            'step': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Instruction'}),
        }

class CustomUserCreation(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_pic']

class CustomUserUpdate(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_pic']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )