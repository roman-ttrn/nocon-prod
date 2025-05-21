# forms.py
from django import forms
from .models import *

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [
            'name', 'description', 'rarity', 'danger', 'power',
            'health', 'speed', 'intelligence', 'luck', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        stats = ['danger', 'power', 'health', 'speed', 'intelligence', 'luck']
        for field in stats:
            value = cleaned_data.get(field)
            if value is not None and not (0 <= value <= 100):
                self.add_error(field, 'Значение должно быть от 0 до 100.')

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название плана'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Введите описание',
                'rows': 5
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-file'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 255:
            raise forms.ValidationError("Название не может быть длиннее 255 символов.")
        return name

