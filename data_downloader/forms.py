from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe


class DateSelectionForm(forms.Form):
    tailwind_class = """
        block text-gray-700 text-5xl lg:text-lg font-bold mb-16 lg:mb-4
    """
    date1 = forms.DateField(label=mark_safe('<br /> From:'), widget=forms.DateInput(attrs={
        'class': tailwind_class,
        'type': 'date'
    }))
    date2 = forms.DateField(label=mark_safe('<br /> To:'), widget=forms.DateInput(attrs={
        'class': tailwind_class,
        'type': 'date'
    }))

