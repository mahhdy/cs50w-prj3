from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',
                  'password1', 'password2', 'avatar', )
        help_texts = {
            'password1': _('Use Strong Password.'),
            'password2': _('Confirm the Exact Password'),
        }

