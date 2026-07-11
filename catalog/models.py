from django.db import models
from accounts.models import CustomUser

COVER_GRADIENTS = [
    'linear-gradient(135deg,#06b6d4,#8b5cf6)',
    'linear-gradient(135deg,#ec4899,#f59e0b)',
    'linear-gradient(135deg,#10b981,#06b6d4)',
    'linear-gradient(135deg,#f43f5e,#8b5cf6)',
    'linear-gradient(135deg,#0ea5e9,#22d3ee)',
    'linear-gradient(135deg,#a3e635,#10b981)',
    'linear-gradient(135deg,#f59e0b,#f43f5e)',
    'linear-gradient(135deg,#8b5cf6,#ec4899)',
    'linear-gradient(135deg,#e879f9,#22d3ee)',
    'linear-gradient(135deg,#fb7185,#fbbf24)',
]

def gradient_for(pk):
    return COVER_GRADIENTS[(pk or 0) % len(COVER_GRADIENTS)]

GENRE_COLORS = {
    'Pop':         'linear-gradient(135deg,#be185d,#ec4899,#f9a8d4)',
    'Rock':        'linear-gradient(135deg,#dc2626,#f97316,#f59e0b)',
    'Hip-Hop':     'linear-gradient(135deg,#6d28d9,#8b5cf6,#a855f7)',
    'Elettronica': 'linear-gradient(135deg,#2563eb,#06b6d4,#22d3ee)',
    'Indie':       'linear-gradient(135deg,#15803d,#22c55e,#84cc16)',
}

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    @property
    def cover_gradient(self):
        return GENRE_COLORS.get(self.name, gradient_for(self.pk))

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)

    @property
    def cover_gradient(self):
        return gradient_for(self.pk)

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

    @property
    def cover_gradient(self):
        return gradient_for(self.pk)

    @property
    def total_duration(self):
        total = sum(song.duration for song in self.songs.all())
        minutes = total // 60
        seconds = total % 60
        return f'{minutes}:{seconds:02d}'

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
    lyrics = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='added_songs')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration_display(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f'{minutes}:{seconds:02d}'

    @property
    def cover_gradient(self):
        if self.genre:
            return self.genre.cover_gradient
        return gradient_for(self.pk)

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

    @property
    def cover_gradient(self):
        return gradient_for(self.pk)

    def __str__(self):
        return f'{self.name} ({self.owner.username})'
