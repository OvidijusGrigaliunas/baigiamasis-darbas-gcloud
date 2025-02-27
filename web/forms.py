from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe


class UserLoginForm(forms.Form):
    tailwind_class = """
        block text-gray-700 text-5xl lg:text-lg font-bold mb-16 lg:mb-4
    """
    username = forms.CharField(label=mark_safe('<br /> User:'), widget=forms.TextInput(attrs={
        'class': tailwind_class
    }))
    password = forms.CharField(label=mark_safe('<br /> Password:'), widget=forms.PasswordInput(attrs={
        'class': tailwind_class
    }))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = """
                            block text-gray-700 text-5xl lg:text-lg font-bold mb-16 lg:mb-4
                        """


class UserDataForm(forms.Form):
    tailwind_class = """
                block text-gray-700 text-5xl lg:text-lg font-bold mb-16 lg:mb-4
            """
    height = forms.FloatField(label=mark_safe('<br /> Height:'), widget=forms.NumberInput(attrs={
        'class': tailwind_class
    }))
    weight = forms.FloatField(label=mark_safe('<br /> Weight:'), widget=forms.NumberInput(attrs={
        'class': tailwind_class
    }))
    birthdate = forms.CharField(label=mark_safe('<br /> Birthdate:'), widget=forms.DateInput(attrs={
        'class': tailwind_class
    }))


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
