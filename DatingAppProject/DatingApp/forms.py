from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from DatingApp.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name', 'second_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'second_name')