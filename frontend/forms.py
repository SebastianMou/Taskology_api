from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api.models import Profile, Interest


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
        return user

class ProfileForm(forms.ModelForm):
    INTEREST_CHOICES = [
        ('Get fit', 'Get fit'),
        ('Lose weight', 'Lose weight'),
        ('Build muscle', 'Build muscle'),
        ('Run a marathon', 'Run a marathon'),
        ('Eat healthier', 'Eat healthier'),
        ('Quit smoking', 'Quit smoking'),
        ('Reduce stress', 'Reduce stress'),
        ('Improve sleep quality', 'Improve sleep quality'),
        ('Get a promotion', 'Get a promotion'),
        ('Change careers', 'Change careers'),
        ('Start a business', 'Start a business'),
        ('Improve skills', 'Improve skills'),
        ('Network with professionals', 'Network with professionals'),
        ('Achieve work-life balance', 'Achieve work-life balance'),
        ('Learn a new language', 'Learn a new language'),
        ('Get a degree', 'Get a degree'),
        ('Read more books', 'Read more books'),
        ('Take online courses', 'Take online courses'),
        ('Attend workshops or seminars', 'Attend workshops or seminars'),
        ('Develop a new hobby', 'Develop a new hobby'),
        ('Travel to new places', 'Travel to new places'),
        ('Volunteer for a cause', 'Volunteer for a cause'),
        ('Improve time management', 'Improve time management'),
        ('Enhance creativity', 'Enhance creativity'),
        ('Build self-confidence', 'Build self-confidence'),
        ('Practice mindfulness or meditation', 'Practice mindfulness or meditation'),
        ('Save more money', 'Save more money'),
        ('Reduce debt', 'Reduce debt'),
        ('Invest in stocks', 'Invest in stocks'),
        ('Buy a house', 'Buy a house'),
        ('Plan for retirement', 'Plan for retirement'),
        ('Create a budget', 'Create a budget'),
        ('Improve family relationships', 'Improve family relationships'),
        ('Make new friends', 'Make new friends'),
        ('Spend more quality time with loved ones', 'Spend more quality time with loved ones'),
        ('Strengthen romantic relationships', 'Strengthen romantic relationships'),
        ('Organize home space', 'Organize home space'),
        ('Renovate home', 'Renovate home'),
        ('Create a garden', 'Create a garden'),
        ('Adopt a pet', 'Adopt a pet'),
        ('Write a book', 'Write a book'),
        ('Learn to play an instrument', 'Learn to play an instrument'),
        ('Improve public speaking skills', 'Improve public speaking skills'),
        ('Meditate daily', 'Meditate daily'),
        ('Learn to cook', 'Learn to cook'),
        ('Practice yoga', 'Practice yoga'),
        ('Travel to all continents', 'Travel to all continents'),
        ('Complete a triathlon', 'Complete a triathlon'),
        ('Learn to code', 'Learn to code'),
        ('Start a blog or vlog', 'Start a blog or vlog')
    ]



    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkmark'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['phone_number', 'interests']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            profile.interests.clear()
            for interest in self.cleaned_data['interests']:
                interest_obj, created = Interest.objects.get_or_create(name=interest)
                profile.interests.add(interest_obj)
        return profile
