from django import forms
from songeek_project.models import Song, Album, UserProfile
from django.contrib.auth.models import User

class AlbumForm(forms.ModelForm):
    name = forms.CharField(max_length=128,help_text="Please enter the Album name.")
    artist = forms.CharField(max_length=128, help_text="Please enter Artist name.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Album
        fields = ('name', 'artist', 'cover')

class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the song name")
    length = forms.DurationField(help_text="Please enter the length of the song.", initial=0)
    listens = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    class Meta:
        model = Song
        exclude = ('album',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)