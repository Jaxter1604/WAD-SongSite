from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from songeek_project.forms import AlbumForm, SongForm, UserForm, UserProfileForm, PlaylistForm, SongToPlaylistForm
from songeek_project.models import Album, Song, Playlist

def index(request):

    song_list = Song.objects.order_by('-likes')[:5]
    albums = Album.objects.all()

    context_dict = {}
    context_dict['songs'] = song_list
    context_dict['albums'] = albums

    return render(request, 'songeek/index.html', context = context_dict)

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
            print(f"Invlaid login details: {username}, {password}")
            return HttpResponse("Invlaid login details supplied.")

    else:
        return render(request, 'songeek/login.html')

def add_song_to_playlist(request):
    if request.method == 'POST':
        form = SongToPlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.cleaned_data['playlist']
            song = form.cleaned_data['song']
            new_song = form.cleaned_data['new_song']
            album = form.cleaned_data['album']
            new_album = form.cleaned_data['new_album']
            artist = form.cleaned_data['artist']
            new_image = form.cleaned_data['new_image']

            if not Song:
                if not album:
                    album, created = Album.objects.get_or_create(
                        name = new_album,
                        artist = artist,
                        defaults = {'slug': slugify(new_album),
                                    'cover': new_image}
                    )

                song, created = Song.objects.get_or_create(
                    album = album,
                    title = new_song
                )
            
            playlist.songs.add(song)
            #change to direct to playlist view when added
            return redirect('/songeek/', playlist.slug)

        else:
            form = SongToPlaylistForm()
    
    return render(request, 'songeek/add_song_to_playlist.html', {'form': form})


#example of returning album page with detail
# def album_detail(request, album_id):
#     album = get_object_or_404(Album, id=album_id)
#     return render(request, 'albums/album_detail.html', {'album': album})