from django import forms
from songeek_project.models import Song, Album, Playlist, UserProfile
from django.contrib.auth.models import User

class AlbumForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the Album name:")
    artist = forms.CharField(max_length=128, help_text="Please enter Artist name:")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Album
        fields = ('name', 'artist', 'cover')

class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the song name:")
    length = forms.DurationField(help_text="Please enter the length of the song:", initial=0)
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

class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=128, required=True, help_text="Enter Playlist name")
    
    class Meta:
        model = Playlist
        fields = ('name', 'cover')

class SongToPlaylistForm(forms.ModelForm):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.all(), help_text="Select a Playlist")
    song = forms.ModelChoiceField(queryset=Song.objects.all(), required=False, help_text="Choose a song or enter a new one below")
    new_song = forms.CharField(max_length=128, required=False, help_text="Enter a new song title (If not selecting above)")
    album = forms.ModelChoiceField(queryset=Album.objects.all(), required=False, help_text="Select an album if adding a new song (or create a new album below)")
    new_album = forms.CharField(max_length=128, required=False, help_text="Enter a new album name (If not selecting above)")
    new_image = forms.ImageField(required=False, help_text="Upload an image if making a new album")
    artist = forms.CharField(max_length=128, required=False, help_text="Required only if adding a new album")

    def clean(self):
        cleaned_data = super().clean()
        song = cleaned_data.get("song")
        new_song = cleaned_data.get("new_song")
        album = cleaned_data.get("album")
        new_album = cleaned_data.get("new_album")
        new_image = cleaned_data.get('new_image')
        artist = cleaned_data.get("artist")

        # Ensure an existing song has an album
        if song and not song.album:
            raise forms.ValidationError("Selected song must belong to an album.")

        # If a new song is provided, an album is required
        if new_song and not (album or new_album):
            raise forms.ValidationError("A new song must be linked to an existing or new album.")

        if new_image and not album:
            raise forms.ValidationError("A new album should have an album cover.")

        return cleaned_data