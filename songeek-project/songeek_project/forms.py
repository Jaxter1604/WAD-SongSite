from django import forms
from songeek_project.models import Song, Album, Playlist, UserProfile, Review
from django.contrib.auth.models import User

# Basic add album form
# needs some adjustments to how questions are asked
# no prompt for cover image
# works via user testing
class AlbumForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the Album name:")
    artist = forms.CharField(max_length=128, help_text="Please enter Artist name:")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Album
        fields = ('name', 'artist', 'cover')

# basic form layout similar to album
# minor testing needed especially with length field
# listens will be set by admin in background or by script
class SongForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the song name:")
    length = forms.DurationField(help_text="Please enter the length of the song:", initial=0)
    listens = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    class Meta:
        model = Song
        exclude = ('album',)

# user forms taken from rango
# tested and working by user
#need unit tests
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

# create a new playlist and uploiad a cover image
# Playlist is assigned to user profile and only
# callable from that user
class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=128, required=True, help_text="Enter Playlist name")
    
    class Meta:
        model = Playlist
        fields = ('name', 'cover')

# add a song to playlist
# current form lets you choose playlist which we might want to keep
# if adding songs from profile
# otheriwse only add songs when in current playlist and remove playlist field

#current form checks:
#   - does the song exist
#   - if a new song then it must be in an album
#   - does the album exist
#   - if new album, insert a cover image

# this form may contain the most issues but can only test when page made
class SongToPlaylistForm(forms.ModelForm):
    song = forms.ModelChoiceField(queryset=Song.objects.all(), required=False, help_text="Choose a song or enter a new one below")
    new_song = forms.CharField(max_length=128, required=False, help_text="Enter a new song title (If not selecting above)")
    album = forms.ModelChoiceField(queryset=Album.objects.all(), required=False, help_text="Select an album if adding a new song (or create a new album below)")
    new_album = forms.CharField(max_length=128, required=False, help_text="Enter a new album name (If not selecting above)")
    new_image = forms.ImageField(required=False, help_text="Upload an image if making a new album")
    artist = forms.CharField(max_length=128, required=False, help_text="Required only if adding a new album")

    # formatting for this class is needed in the html file
    # to distinguish between "new song" fields and
    # existsing song fields etc
    class Meta:
        model = Playlist
        fields = ('song', 'album', 'new_song', 'new_album', 'artist')

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

        # if an image is provided then we need to make a new album
        if new_image and not new_album:
            raise forms.ValidationError("A new album should have an album cover.")

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        