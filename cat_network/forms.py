from django.contrib.auth.forms import UserCreationForm
from django import forms

from cat_network.models import CatUser


class CatUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CatUser
        fields = UserCreationForm.Meta.fields + ("first_name", "age", "profile_picture")


class PostSearchForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search by title'}),
    )


class CatSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search by username'}),
    )