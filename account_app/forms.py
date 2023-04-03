from django.forms import ModelForm
from django.contrib.auth.models import User


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        # all basic fields
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
