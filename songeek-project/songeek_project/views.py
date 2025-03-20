from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from songeek_project.forms import AlbumForm, SongForm, UserForm, UserProfileForm, PlaylistForm, SongToPlaylistForm, ReviewForm
from songeek_project.models import Album, Song, Playlist, Review

def index(request):

    song_list = Song.objects.order_by('-listens')[:5]
    albums = Album.objects.all()[:8]
    
    user_playlists = None
    if request.user.is_authenticated:
        user_playlists = Playlist.objects.filter(user=request.user)[:4]

    context_dict = {
        'songs': song_list,
        'albums': albums,
        'user_playlists': user_playlists,
    }

    return render(request, 'songeek/index.html', context=context_dict)

@login_required
def add_album(request):
    form = AlbumForm()

    if request.method =='POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/songeek/')
        else:
            print(form.errors)
    return render(request, 'songeek/add_album.html', {'form': form})

@login_required
def add_song_to_album(request, album_name_slug):
    try:
        album = Album.objects.get(slug=album_name_slug)
    except Album.DoesNotExist:
        album = None
    form = SongForm()

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.album = album
            song.save()
            return redirect(reverse('songeek:show_album',
                    kwargs={'album_name_slug': album_name_slug}))
        else:
            print(form.errors)
    return render(request, 'songeek/add_song_to_album.html', {'form': form, 'album': album})

def show_song(request, song_id):
    from django.shortcuts import get_object_or_404
    
    song = get_object_or_404(Song, id=song_id)
    reviews = Review.objects.filter(song=song)
    
    form = ReviewForm() if request.user.is_authenticated else None

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.song = song
            review.user = request.user
            review.save()
            return redirect('songeek:show_song', song_id=song.id)

    return render(request, 'songeek/song.html', {
        'song': song,
        'reviews': reviews,
        'form': form
    })

def show_album(request, album_name_slug):
    context_dict = {}

    try:
        album = Album.objects.get(slug=album_name_slug)
        songs = Song.objects.filter(album=album)
        reviews = Review.objects.filter(album=album)
        form = ReviewForm()

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.album = album
                review.user  = request.user
                review.save()
            return redirect(reverse('songeek:show_album',
                    kwargs={'album_name_slug': album_name_slug}))

        context_dict['songs'] = songs
        context_dict['album'] = album
        context_dict['reviews'] = reviews
        context_dict['form'] = form
    except Album.DoesNotExist:
        context_dict['songs'] = None
        context_dict['album'] = None
        context_dict['reviews'] = None
        context_dict['form'] = None

    return render(request, 'songeek/album.html', context=context_dict)

def album_list(request):
    
    albums = Album.objects.all()

    context_dict = {}
    context_dict['albums'] = albums

    return render(request, 'songeek/album_list.html', context = context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            login(request, user)
            #return redirect('homepage')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'songeek/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('songeek:index'))
            else:
                return HttpResponse("Your Songeek account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'songeek/login.html')

#def homepage(request):
#    return render(request, 'homepage.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('songeek:index'))

@login_required
def new_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('/songeek/')  
        else:
            print(form.errors)  

    return render(request, 'songeek/new_playlist.html', {'form': form})


def add_song_to_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('/songeek/')  
        else:
            print(form.errors)  

    return render(request, 'songeek/new_playlist.html', {'form': form})

@login_required
def show_playlist(request, playlist_name_slug):
    context_dict = {}

    try:
        playlist = Playlist.objects.get(slug=playlist_name_slug, user=request.user)
        songs = playlist.songs.all()

        context_dict['songs'] = songs
        context_dict['playlist'] = playlist

    except Album.DoesNotExist:
        context_dict['songs'] = None
        context_dict['playlist'] = None

    return render(request, 'songeek/playlist.html', context=context_dict)
    
@login_required
def add_song_to_playlist(request, playlist_name_slug):

    try:
        playlist = Playlist.objects.get(slug=playlist_name_slug, user=request.user)
    except Playlist.DoesNotExist:
        return HttpResponse("Playlist not found")

    form = SongToPlaylistForm()
    if request.method == 'POST':
        form = SongToPlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            song = form.cleaned_data['song']
            new_song = form.cleaned_data['new_song']
            length = form.cleaned_data['length']
            album = form.cleaned_data['album']
            new_album = form.cleaned_data['new_album']
            artist = form.cleaned_data['artist']
            new_image = form.cleaned_data['new_image']

            if not song:
                if not album:
                    album, created = Album.objects.get_or_create(
                        name = new_album,
                        artist = artist,
                        defaults = {'slug': slugify(new_album),
                                    'cover': new_image}
                    )

                song, created = Song.objects.get_or_create(
                    album = album,
                    title = new_song,
                    length = length
                )
            
            playlist.songs.add(song)
            #change to direct to playlist view when added
            return redirect(reverse('songeek:show_playlist',
                    kwargs={'playlist_name_slug': playlist_name_slug}))
        else:
            print(form.errors)
    
    return render(request, 'songeek/add_song_to_playlist.html', {'form': form, 'playlist': playlist})

#filter playlists by user id and return
@login_required
def profile(request):
    playlists = Playlist.objects.filter(user=request.user)

    context_dict = {'playlists': playlists}
    return render(request, 'songeek/profile.html', context=context_dict)

def search_results(request):
    query = request.GET.get('q', '')

    if query:
        albums = Album.objects.filter(name__icontains=query)
        songs = Song.objects.filter(title__icontains=query)
    else:
        albums = []
        songs = []

    context_dict = {
        'query': query,
        'albums': albums,
        'songs': songs
    }

    return render(request, 'songeek/search_results.html', context=context_dict)