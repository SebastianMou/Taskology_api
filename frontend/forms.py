from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api.models import Profile, Interest, Goal


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
        ('Achieve work-life balance', 'Achieve work-life balance'),
        ('Advance in career', 'Advance in career'),
        ('Build a personal brand', 'Build a personal brand'),
        ('Improve fitness levels', 'Improve fitness levels'),
        ('Develop a healthy eating plan', 'Develop a healthy eating plan'),
        ('Master a new skill', 'Master a new skill'),
        ('Cultivate a hobby', 'Cultivate a hobby'),
        ('Improve mental health', 'Improve mental health'),
        ('Establish a daily routine', 'Establish a daily routine'),
        ('Enhance digital literacy', 'Enhance digital literacy'),
        ('Improve financial literacy', 'Improve financial literacy'),
        ('Volunteer regularly', 'Volunteer regularly'),
        ('Reduce screen time', 'Reduce screen time'),
        ('Improve sleep hygiene', 'Improve sleep hygiene'),
        ('Develop emotional intelligence', 'Develop emotional intelligence'),
        ('Improve negotiation skills', 'Improve negotiation skills'),
        ('Enhance leadership skills', 'Enhance leadership skills'),
        ('Learn mindfulness practices', 'Learn mindfulness practices'),
        ('Develop a personal development plan', 'Develop a personal development plan'),
        ('Improve organizational skills', 'Improve organizational skills'),
        ('Strengthen family bonds', 'Strengthen family bonds'),
        ('Enhance social skills', 'Enhance social skills'),
        ('Build a personal library', 'Build a personal library'),
        ('Improve environmental sustainability habits', 'Improve environmental sustainability habits'),
        ('Learn to manage stress', 'Learn to manage stress'),
        ('Enhance problem-solving skills', 'Enhance problem-solving skills'),
        ('Develop a creative project', 'Develop a creative project'),
        ('Achieve specific fitness milestones (e.g., run 5K)', 'Achieve specific fitness milestones (e.g., run 5K)'),
        ('Improve study habits', 'Improve study habits'),
        ('Learn time management techniques', 'Learn time management techniques'),
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
    
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'  # or list specific fields if needed
