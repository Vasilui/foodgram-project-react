from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password', 'email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password', 'email',)
