import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicstream.settings')
django.setup()

from accounts.models import CustomUser
from catalog.models import Genre, Artist, Album, Song, Playlist

print("Pulizia dati esistenti...")
Song.objects.all().delete()
Album.objects.all().delete()
Artist.objects.all().delete()
Genre.objects.all().delete()
Playlist.objects.all().delete()
CustomUser.objects.all().delete()

print("Creazione generi...")
pop         = Genre.objects.create(name="Pop",         description="Musica pop internazionale")
rock        = Genre.objects.create(name="Rock",        description="Rock classico e moderno")
hiphop      = Genre.objects.create(name="Hip-Hop",     description="Rap e hip-hop")
elettronica = Genre.objects.create(name="Elettronica", description="Dance, house, techno")
indie       = Genre.objects.create(name="Indie",       description="Musica indipendente")

print("Creazione artisti...")
weeknd      = Artist.objects.create(name="The Weeknd",    bio="Artista canadese, icona del pop dark.")
dua         = Artist.objects.create(name="Dua Lipa",      bio="Cantautrice britannica-albanese, regina del pop dance.")
nirvana     = Artist.objects.create(name="Nirvana",       bio="Band grunge di Seattle, simbolo degli anni '90.")
arctic      = Artist.objects.create(name="Arctic Monkeys",bio="Band indie rock di Sheffield, UK.")
kendrick    = Artist.objects.create(name="Kendrick Lamar",bio="Rapper di Compton, uno dei più influenti della sua generazione.")
daft        = Artist.objects.create(name="Daft Punk",     bio="Duo elettronico francese, pionieri della French house.")
queen       = Artist.objects.create(name="Queen",         bio="Band rock britannica, una delle più iconiche della storia.")
eagles      = Artist.objects.create(name="Eagles",        bio="Band rock americana degli anni '70.")
acdc        = Artist.objects.create(name="AC/DC",         bio="Band rock australiana, simbolo dell'hard rock.")
drake       = Artist.objects.create(name="Drake",         bio="Rapper e cantante canadese, artista più ascoltato al mondo.")
eminem      = Artist.objects.create(name="Eminem",        bio="Rapper di Detroit, tra i più venduti della storia.")
m83         = Artist.objects.create(name="M83",           bio="Progetto dream pop/shoegaze francese.")
killers     = Artist.objects.create(name="The Killers",   bio="Band indie rock di Las Vegas.")
laroi       = Artist.objects.create(name="The Kid LAROI", bio="Rapper australiano, collaborazione con Justin Bieber.")

print("Creazione album...")
after_hours      = Album.objects.create(name="After Hours",             artist=weeknd)
future_nostalgia = Album.objects.create(name="Future Nostalgia",        artist=dua)
nevermind        = Album.objects.create(name="Nevermind",               artist=nirvana)
am               = Album.objects.create(name="AM",                      artist=arctic)
damn             = Album.objects.create(name="DAMN.",                   artist=kendrick)
discovery        = Album.objects.create(name="Discovery",               artist=daft)
a_night          = Album.objects.create(name="A Night at the Opera",    artist=queen)
hotel_cal        = Album.objects.create(name="Hotel California",        artist=eagles)
the_razors       = Album.objects.create(name="The Razors Edge",         artist=acdc)
scorpion         = Album.objects.create(name="Scorpion",                artist=drake)
mile8            = Album.objects.create(name="8 Mile",                  artist=eminem)
hurry_up         = Album.objects.create(name="Hurry Up We're Dreaming", artist=m83)
hot_fuss         = Album.objects.create(name="Hot Fuss",                artist=killers)
fck_love         = Album.objects.create(name="F*CK LOVE 3",             artist=laroi)

print("Creazione utenti demo...")
listener = CustomUser.objects.create_user(
    username='user_demo', password='user12345',
    email='user@demo.com', role='listener',
    bio='Appassionata di musica, ascolto tutto!',
)
curator = CustomUser.objects.create_user(
    username='curator_demo', password='curator12345',
    email='curator@demo.com', role='curator',
    bio='Curator della libreria musicale.',
)
admin = CustomUser.objects.create_superuser(
    username='admin_demo', password='admin12345',
    email='admin@demo.com',
)

print("Creazione canzoni...")
songs_data = [
    # title, artist, album, genre, duration_sec
    ("Blinding Lights",                          weeknd,   after_hours,      pop,         200),
    ("Save Your Tears",                          weeknd,   after_hours,      pop,         215),
    ("In Your Eyes",                             weeknd,   after_hours,      pop,         238),
    ("Heartless",                                weeknd,   after_hours,      pop,         187),
    ("Levitating",                               dua,      future_nostalgia, pop,         203),
    ("Don't Start Now",                          dua,      future_nostalgia, pop,         183),
    ("Physical",                                 dua,      future_nostalgia, pop,         193),
    ("Stay",                                     laroi,    fck_love,         pop,         141),
    ("Smells Like Teen Spirit",                  nirvana,  nevermind,        rock,        301),
    ("Come as You Are",                          nirvana,  nevermind,        rock,        219),
    ("Lithium",                                  nirvana,  nevermind,        rock,        257),
    ("Bohemian Rhapsody",                        queen,    a_night,          rock,        354),
    ("Hotel California",                         eagles,   hotel_cal,        rock,        391),
    ("Thunderstruck",                            acdc,     the_razors,       rock,        292),
    ("God's Plan",                               drake,    scorpion,         hiphop,      198),
    ("HUMBLE.",                                  kendrick, damn,             hiphop,      177),
    ("DNA.",                                     kendrick, damn,             hiphop,      185),
    ("LOYALTY.",                                 kendrick, damn,             hiphop,      228),
    ("Lose Yourself",                            eminem,   mile8,            hiphop,      326),
    ("Midnight City",                            m83,      hurry_up,         elettronica, 244),
    ("One More Time",                            daft,     discovery,        elettronica, 320),
    ("Harder Better Faster Stronger",            daft,     discovery,        elettronica, 224),
    ("Digital Love",                             daft,     discovery,        elettronica, 301),
    ("Do I Wanna Know?",                         arctic,   am,               indie,       272),
    ("R U Mine?",                                arctic,   am,               indie,       201),
    ("Why'd You Only Call Me When You're High?", arctic,   am,               indie,       202),
    ("Mr. Brightside",                           killers,  hot_fuss,         indie,       222),
]

songs = []
for title, artist, album, genre, duration in songs_data:
    song = Song.objects.create(
        title=title, artist=artist, album=album,
        genre=genre, duration=duration, added_by=curator,
    )
    songs.append(song)

print("Creazione playlist demo...")
p1 = Playlist.objects.create(name="I miei preferiti", owner=listener)
p1.songs.add(songs[0], songs[4], songs[11], songs[14], songs[26])

p2 = Playlist.objects.create(name="Workout Mix", owner=listener)
p2.songs.add(songs[1], songs[8], songs[20], songs[18])

p3 = Playlist.objects.create(name="Serata indie", owner=curator)
p3.songs.add(songs[23], songs[24], songs[25], songs[26])

p4 = Playlist.objects.create(name="Viaggio in macchina", owner=curator)
p4.songs.add(songs[20], songs[21], songs[22], songs[11], songs[12])

print(f"\n✅ Database popolato con successo!")
print(f"   {Artist.objects.count()} artisti, {Album.objects.count()} album, {Song.objects.count()} canzoni, {Genre.objects.count()} generi, {Playlist.objects.count()} playlist")
print("\nAccount demo:")
print("  user_demo    / user12345    → Listener")
print("  curator_demo / curator12345 → Curator")
print("  admin_demo   / admin12345   → Admin (superuser)")
