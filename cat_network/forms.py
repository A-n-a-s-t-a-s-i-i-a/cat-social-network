from django.contrib.auth.forms import UserCreationForm

from cat_network.models import CatUser


class CatUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CatUser
        fields = UserCreationForm.Meta.fields + ("first_name", "age", "profile_picture")