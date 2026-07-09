# MusicStream

**Studente:** Gaia Baldanzi — A.A. 2025/2026
**Esame:** Progettazione e Produzione Multimediale (Back-end)
**Tipo di progetto:** Full-Stack Web Application
**Framework:** Django 4.2 (Python)
**Track:** 4 — Music Streaming Service

---

## Descrizione

MusicStream è un servizio di streaming musicale navigabile da browser. Gli utenti possono
esplorare un catalogo di canzoni, artisti, album e generi, cercare contenuti, e — a seconda
del proprio ruolo — creare playlist personali o gestire l'intera libreria musicale.

---

## Link al sito online

**https://musicstream-iuvd.onrender.com**

> Nota: il sito è ospitato sul piano gratuito di Render. Alla prima apertura dopo un periodo
> di inattività può impiegare ~50 secondi a caricare, perché l'istanza si riavvia.

---

## Funzionalità per ruolo

**Listener** (utente standard)
- Sfoglia canzoni, artisti, album e generi
- Ricerca globale per testo e categoria
- Crea, modifica ed elimina le proprie playlist
- Aggiunge e rimuove canzoni dalle playlist
- Modifica il proprio profilo e avatar

**Curator** (ruolo avanzato)
- Tutte le funzionalità del Listener
- Aggiunge, modifica ed elimina canzoni (con testo)
- Aggiunge artisti, album e generi

**Accessi differenziati:** l'interfaccia cambia in base al ruolo (voci di menu, pulsanti e
azioni visibili). Quando un utente prova un'azione non consentita, riceve un messaggio di errore.

---

## Tecnologie

- Python 3.9 / Django 4.2
- Database SQLite (`db.sqlite3`, incluso e pre-popolato)
- Bootstrap 5 + Bootstrap Icons
- Tom Select (menu a tendina ricercabili)
- Gunicorn + WhiteNoise (deploy in produzione)

---

## Database

Il repository include il file **`db.sqlite3`** già pre-popolato con dati di esempio
(14 artisti, 14 album, 27 canzoni, 5 generi, 4 playlist) e gli account demo elencati sotto.

---

## Account demo

| Username | Password | Ruolo |
|---|---|---|
| `user_demo` | `user12345` | Listener |
| `curator_demo` | `curator12345` | Curator |
| `admin_demo` | `admin12345` | Superuser (accesso al pannello `/admin/`) |

---

## Installazione ed esecuzione in locale

```bash
# 1. Clona il repository
git clone https://github.com/gaiabaldanzi-unifi/musicstream.git
cd musicstream

# 2. Crea e attiva il virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Applica le migrazioni
python manage.py migrate

# 5. (Opzionale) Ripopola il database con dati di esempio
python populate_db.py

# 6. Avvia il server
python manage.py runserver
```

Apri il browser su `http://127.0.0.1:8000`

---

## Scenario di test (dal browser)

1. Apri il sito e fai **login** come `curator_demo` / `curator12345`
2. Vai su **Canzoni** e apri una canzone: vedrai i dettagli e il testo
3. Clicca **Aggiungi canzone**, compila il form e salva → la nuova canzone compare nel catalogo
4. Crea una **playlist** e aggiungici qualche canzone
5. Fai **logout** e accedi come `user_demo` / `user12345` (Listener)
6. Prova ad aprire `/canzoni/aggiungi/`: l'azione è **negata** e appare un messaggio di errore
   (il Listener non può gestire il catalogo) → conferma che i permessi funzionano

---

## Struttura del progetto

```
musicstream/
    accounts/       → app per utenti, autenticazione e profili
    catalog/        → app per canzoni, artisti, album, generi, playlist
    templates/      → template HTML
    media/          → file caricati dagli utenti
    db.sqlite3      → database SQLite pre-popolato
    requirements.txt
    build.sh        → script di build per il deploy
    manage.py
```
