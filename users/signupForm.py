from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class NewUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        help_texts = {
            'email': None,
            'username': None,
            'first_name': None,
            'last_name': None,
            'password1': None,
            'password2': None,
        }

    


