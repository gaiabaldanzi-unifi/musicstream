from django.db import models
from accounts.models import CustomUser

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='albums'
    )
    cover = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        related_name='songs'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='songs'
    )
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')
    duration = models.PositiveIntegerField(help_text='Durata in secondi')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='added_songs')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration_display(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f'{minutes}:{seconds:02d}'

    def __str__(self):
        return f'{self.title} — {self.artist}'

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField(Song, blank=True, related_name='playlists')
    cover = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_duration(self):
        total = sum(song.duration for song in self.songs.all())
        minutes = total // 60
        seconds = total % 60
        return f'{minutes}:{seconds:02d}'

    def __str__(self):
        return f'{self.name} ({self.owner.username})'
