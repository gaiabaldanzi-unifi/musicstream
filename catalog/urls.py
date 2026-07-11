from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('canzoni/', views.SongListView.as_view(), name='song_list'),
    path('cerca/', views.search, name='search'),
    path('artisti/', views.ArtistListView.as_view(), name='artist_list'),
    path('artisti/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('artisti/nuovo/', views.artist_create, name='artist_create'),
    path('artisti/<int:pk>/modifica/', views.artist_update, name='artist_update'),
    path('artisti/<int:pk>/elimina/', views.artist_delete, name='artist_delete'),
    path('generi/', views.genre_list, name='genre_list'),
    path('generi/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('generi/nuovo/', views.genre_create, name='genre_create'),
    path('generi/<int:pk>/modifica/', views.genre_update, name='genre_update'),
    path('album/', views.album_list, name='album_list'),
    path('album/<int:pk>/', views.album_detail, name='album_detail'),
    path('album/nuovo/', views.album_create, name='album_create'),
    path('album/<int:pk>/modifica/', views.album_update, name='album_update'),
    path('album/<int:pk>/elimina/', views.album_delete, name='album_delete'),
    path('canzoni/<int:pk>/', views.song_detail, name='song_detail'),
    path('canzoni/aggiungi/', views.song_create, name='song_create'),
    path('canzoni/<int:pk>/modifica/', views.song_update, name='song_update'),
    path('canzoni/<int:pk>/elimina/', views.song_delete, name='song_delete'),
    path('playlist/', views.playlist_list, name='playlist_list'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/crea/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:pk>/aggiungi/<int:song_pk>/', views.playlist_add_song, name='playlist_add_song'),
    path('playlist/<int:pk>/rimuovi/<int:song_pk>/', views.playlist_remove_song, name='playlist_remove_song'),
    path('playlist/<int:pk>/modifica/', views.playlist_update, name='playlist_update'),
    path('playlist/<int:pk>/elimina/', views.playlist_delete, name='playlist_delete'),
]