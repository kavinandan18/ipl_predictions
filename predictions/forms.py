from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Prediction,Match
from django.contrib.auth.forms import PasswordChangeForm


class CreateMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'date', 'winner']

    def __init__(self, *args, **kwargs):
        super(CreateMatchForm, self).__init__(*args, **kwargs)
        self.fields['winner'].required = False

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['match', 'chosen_winner']

    def __init__(self, *args, **kwargs):
        super(PredictionForm, self).__init__(*args, **kwargs)

        # Hide the 'match' field from the user
        self.fields['match'].widget = forms.HiddenInput()

        # Limit the choices for 'chosen_winner' to teams involved in the match
        match_instance = self.initial.get('match')
        if match_instance:
            if isinstance(match_instance, int):
                match_instance = Match.objects.get(pk=match_instance)
            team1 = match_instance.team1
            team2 = match_instance.team2
            team_choices = [(team1.id, str(team1)), (team2.id, str(team2))]
            self.fields['chosen_winner'].choices = team_choices

        # Optionally, display the match details as plain text
        if match_instance:
            self.fields['match_details'] = forms.CharField(
                required=False,
                disabled=True,
                initial=str(match_instance),
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
            )





class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
        strip=False,
    )

    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
    )


class EditMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'date', 'winner']

    def __init__(self, *args, **kwargs):
        super(EditMatchForm, self).__init__(*args, **kwargs)

        # Limit choices for the 'winner' field to teams involved in the match
        team1 = self.instance.team1
        team2 = self.instance.team2
        team_choices = [(team1.id, str(team1)), (team2.id, str(team2)), (None, '---------')]
        self.fields['winner'].widget = forms.Select(choices=team_choices)

        # Disable team1 and team2 fields
        self.fields['team1'].disabled = True
        self.fields['team2'].disabled = True

        # Add a default value to the 'date' field
        self.fields['date'].widget.attrs['value'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()

        # Remove 'team1' and 'team2' from the cleaned_data
        cleaned_data.pop('team1', None)
        cleaned_data.pop('team2', None)

        winner = cleaned_data.get('winner')

        # Additional validation if needed

        return cleaned_data



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize error messages for the username and password fields
        self.fields['username'].error_messages = {
            'required': 'Username is required. (Maximum 150 characters)',
            'unique': 'A user with that username already exists.',
            'max_length': 'Username cannot be more than 150 characters.'
        }
        self.fields['password1'].error_messages = {
            'required': 'Password is required.',
            'password_mismatch': 'The two password fields did not match.',
            'min_length': 'Password must be at least 8 characters long.',
            'password_too_common': 'This password is too common.',
            'password_entirely_numeric': 'Password cannot be entirely numeric.',
        }

        # Remove the help_text for the password fields
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
