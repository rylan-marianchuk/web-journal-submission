from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



USER_TYPES = [('author', 'Author'), ('editor', 'Editor'), ('reviewer', 'Reviewer')]


class CreateUserForm(UserCreationForm):
    """
    This is the base form to register a user. Inherits from the Django usercreation form.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileDetailsForm(ModelForm):
    """
    Profile will ask for extra info that is not included in the default Django user registration. That is why this
    class inherits from ModelForm, not UserCreationForm
    """
    class Meta:
        # Model is the database object this form should populate
        model = Profile
        # The fields to display on this form
        fields = ['institute', 'discipline', 'role']


