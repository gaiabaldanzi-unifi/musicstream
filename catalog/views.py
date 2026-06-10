from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import Genre, Song, Playlist, Album, Artist
from .forms import SongForm, PlaylistForm, AlbumForm, GenreForm, ArtistForm

def home(request):
    songs = Song.objects.order_by('-created_at')[:6]
    genres = Genre.objects.all()
    return render(request, 'catalog/home.html', {
        'songs': songs,
        'genres': genres,
    })

class SongListView(ListView):
    model = Song
    template_name = 'catalog/song_list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        songs = Song.objects.all()
        query = self.request.GET.get('q')
        genre_id = self.request.GET.get('genre')
        if query:
            songs = songs.filter(
                Q(title__icontains=query) | Q(artist__name__icontains=query)
            )
        if genre_id:
            songs = songs.filter(genre__id=genre_id)
        return songs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['query'] = self.request.GET.get('q', '')
        return context

@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('cat', 'all')
    songs, artists, albums, genres = [], [], [], []
    if query:
        if category in ('all', 'songs'):
            songs = Song.objects.filter(
                Q(title__icontains=query) | Q(artist__name__icontains=query)
            )
        if category in ('all', 'artists'):
            artists = Artist.objects.filter(name__icontains=query)
        if category in ('all', 'albums'):
            albums = Album.objects.filter(
                Q(name__icontains=query) | Q(artist__name__icontains=query)
            )
        if category in ('all', 'genres'):
            genres = Genre.objects.filter(name__icontains=query)
    return render(request, 'catalog/search.html', {
        'query': query,
        'category': category,
        'songs': songs,
        'artists': artists,
        'albums': albums,
        'genres': genres,
    })

def artist_list(request):
    query = request.GET.get('q', '').strip()
    artists = Artist.objects.all().order_by('name')
    if query:
        artists = artists.filter(name__icontains=query)
    return render(request, 'catalog/artist_list.html', {'artists': artists, 'query': query})

def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    songs = artist.songs.order_by('title')
    albums = artist.albums.all()
    return render(request, 'catalog/artist_detail.html', {
        'artist': artist,
        'songs': songs,
        'albums': albums,
    })

@login_required
def artist_create(request):
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono aggiungere artisti.')
        return redirect('catalog:artist_list')
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save()
            messages.success(request, f'Artista "{artist.name}" creato!')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('catalog:artist_detail', pk=artist.pk)
    else:
        form = ArtistForm()
    return render(request, 'catalog/artist_form.html', {'form': form})

def genre_list(request):
    query = request.GET.get('q', '').strip()
    genres = Genre.objects.all().order_by('name')
    if query:
        genres = genres.filter(name__icontains=query)
    return render(request, 'catalog/genre_list.html', {'genres': genres, 'query': query})

def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    songs = genre.songs.order_by('title')
    return render(request, 'catalog/genre_detail.html', {
        'genre': genre,
        'songs': songs,
    })

@login_required
def genre_create(request):
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono aggiungere generi.')
        return redirect('catalog:genre_list')
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            messages.success(request, f'Genere "{genre.name}" creato!')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('catalog:genre_detail', pk=genre.pk)
    else:
        form = GenreForm()
    return render(request, 'catalog/genre_form.html', {'form': form})

def album_list(request):
    query = request.GET.get('q', '').strip()
    albums = Album.objects.all().order_by('name')
    if query:
        albums = albums.filter(Q(name__icontains=query) | Q(artist__name__icontains=query))
    return render(request, 'catalog/album_list.html', {'albums': albums, 'query': query})

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    songs = album.songs.order_by('title')
    return render(request, 'catalog/album_detail.html', {
        'album': album,
        'songs': songs,
    })

@login_required
def album_create(request):
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono aggiungere album.')
        return redirect('catalog:album_list')
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save()
            messages.success(request, f'Album "{album.name}" creato! Ora puoi aggiungerlo a una canzone.')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('catalog:album_detail', pk=album.pk)
    else:
        form = AlbumForm()
    return render(request, 'catalog/album_form.html', {'form': form})

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    user_playlists = []
    if request.user.is_authenticated:
        for pl in request.user.playlists.all():
            user_playlists.append({
                'playlist': pl,
                'has_song': pl.songs.filter(pk=song.pk).exists(),
            })
    return render(request, 'catalog/song_detail.html', {
        'song': song,
        'user_playlists': user_playlists,
    })

@login_required
def song_create(request):
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono aggiungere canzoni.')
        return redirect('catalog:song_list')
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.added_by = request.user
            song.save()
            messages.success(request, 'Canzone aggiunta!')
            return redirect('catalog:song_detail', pk=song.pk)
    else:
        form = SongForm()
    return render(request, 'catalog/song_form.html', {'form': form, 'title': 'Aggiungi canzone'})

@login_required
def song_update(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono modificare canzoni.')
        return redirect('catalog:song_detail', pk=pk)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            messages.success(request, 'Canzone modificata!')
            return redirect('catalog:song_detail', pk=song.pk)
    else:
        form = SongForm(instance=song)
    return render(request, 'catalog/song_form.html', {'form': form, 'title': 'Modifica canzone'})

@login_required
def song_delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if not request.user.is_curator():
        messages.error(request, 'Solo i Curator possono eliminare canzoni.')
        return redirect('catalog:song_detail', pk=pk)
    if request.method == 'POST':
        song.delete()
        messages.success(request, 'Canzone eliminata.')
        return redirect('catalog:song_list')
    return render(request, 'catalog/song_confirm_delete.html', {'song': song})

@login_required
def playlist_list(request):
    query = request.GET.get('q', '').strip()
    playlists = Playlist.objects.filter(owner=request.user)
    if query:
        playlists = playlists.filter(name__icontains=query)
    return render(request, 'catalog/playlist_list.html', {'playlists': playlists, 'query': query})

@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    songs = Song.objects.exclude(playlists=playlist)[:6]
    return render(request, 'catalog/playlist_detail.html', {
        'playlist': playlist,
        'available_songs': songs,
    })

@login_required
def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            messages.success(request, 'Playlist creata!')
            return redirect('catalog:playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm()
    return render(request, 'catalog/playlist_form.html', {'form': form})

@login_required
def playlist_add_song(request, pk, song_pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    song = get_object_or_404(Song, pk=song_pk)
    playlist.songs.add(song)
    messages.success(request, f'"{song.title}" aggiunta alla playlist!')
    next_url = request.GET.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('catalog:playlist_detail', pk=pk)

@login_required
def playlist_remove_song(request, pk, song_pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    song = get_object_or_404(Song, pk=song_pk)
    playlist.songs.remove(song)
    messages.success(request, f'"{song.title}" rimossa dalla playlist!')
    next_url = request.GET.get('next', '')
    if next_url:
        return redirect(next_url)
    return redirect('catalog:playlist_detail', pk=pk)

@login_required
def playlist_update(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Playlist aggiornata!')
            from django.urls import reverse
            return redirect(reverse('catalog:playlist_detail', args=[playlist.pk]) + '?modifica=1')
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'catalog/playlist_form.html', {'form': form, 'playlist': playlist})