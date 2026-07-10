from django import forms
from .models import Song, Playlist, Album, Genre, Artist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'bio', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'artist', 'cover')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        self.fields['artist'].empty_label = '— Seleziona artista —'

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'album', 'genre', 'duration', 'lyrics', 'cover')
        labels = {'lyrics': 'Testo'}
        widgets = {'lyrics': forms.Textarea(attrs={'rows': 8})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
        self.fields['artist'].empty_label = '— Seleziona artista —'
        self.fields['album'].empty_label = '— Nessun album —'
        self.fields['genre'].empty_label = '— Seleziona genere —'
        self.fields['duration'].error_messages = {
            'required': 'Questo campo è obbligatorio e deve contenere solo numeri tra 1 e 3600 (secondi).',
            'invalid': 'Questo campo è obbligatorio e deve contenere solo numeri tra 1 e 3600 (secondi).',
        }

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration is not None and (duration < 1 or duration > 3600):
            raise forms.ValidationError(
                'Questo campo è obbligatorio e deve contenere solo numeri tra 1 e 3600 (secondi).'
            )
        return duration

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('name', 'description', 'cover')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
