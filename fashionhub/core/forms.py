from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Outfit, OutfitImage, Category, Review, Message


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'phone', 'profile_image')


class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ('name', 'description', 'price', 'category', 'image', 'is_active')


class OutfitImageForm(forms.ModelForm):
    class Meta:
        model = OutfitImage
        fields = ('image', 'caption')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('receiver', 'subject', 'body')
