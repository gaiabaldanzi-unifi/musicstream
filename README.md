# MusicStream

Servizio di streaming musicale — Full-Stack Web Application sviluppata con Django 4.2.
Progetto d'esame per il corso di Progettazione e Produzione Multimediale di **Gaia Baldanzi** (matricola 7115020, A.A. 2025/2026).

**Sito online:** https://musicstream-iuvd.onrender.com

---

MusicStream è un'applicazione web che permette di consultare un catalogo di canzoni, artisti, album e generi, di cercare tra i contenuti e di gestire playlist personali. L'accesso alle funzionalità è regolato da un sistema di ruoli: un **Listener** consulta il catalogo e gestisce le proprie playlist, mentre un **Curator** ha tutte le capacità del Listener e in aggiunta gestisce l'intera libreria musicale.

| Capacità | Listener | Curator |
|---|:---:|:---:|
| Sfogliare canzoni, artisti, album e generi | Sì | Sì |
| Ricerca globale per testo e categoria | Sì | Sì |
| Creare e gestire le proprie playlist | Sì | Sì |
| Modificare il proprio profilo | Sì | Sì |
| Creare, modificare ed eliminare canzoni (con testo) | — | Sì |
| Creare, modificare ed eliminare artisti | — | Sì |
| Creare, modificare ed eliminare album | — | Sì |
| Creare e modificare generi | — | Sì |

L'eliminazione di un artista o di un album rimuove anche le relative canzoni. I generi possono essere creati e modificati ma non eliminati.

Il catalogo è interconnesso: dalla pagina di dettaglio di una canzone si può passare direttamente al suo artista, al suo album e al suo genere, e da lì esplorare gli altri contenuti collegati. L'applicazione propone inoltre canzoni consigliate in base al genere e all'artista, sia nella pagina di una canzone sia all'interno di una playlist.

L'interfaccia si adatta al ruolo. Il Curator, ad esempio, vede un pulsante **"Aggiungi canzone"**; all'interno del modulo di inserimento può anche creare un nuovo artista, album o genere, nel caso non siano già presenti nel catalogo.

I dati inseriti vengono validati. Le principali validazioni sono:

- nel modulo di aggiunta di una canzone il menu degli album mostra solo gli album dell'artista selezionato, così da evitare accostamenti incoerenti tra artista e album;
- la durata di una canzone deve essere un numero compreso tra 1 e 3600 secondi (un'ora), altrimenti compare un messaggio di errore;
- i campi obbligatori lasciati vuoti mostrano un errore in stile Django (non il messaggio predefinito del browser);
- la registrazione applica le validazioni standard di Django: robustezza della password, coincidenza delle due password e unicità dello username.

Il database SQLite incluso nel repository (`db.sqlite3`) è già pre-popolato con dati di esempio (14 artisti, 14 album, 27 canzoni, 5 generi e 4 playlist) e con i tre account demo seguenti:

| Username | Password | Ruolo |
|---|---|---|
| user_demo | user12345 | Listener |
| curator_demo | curator12345 | Curator |
| admin_demo | admin12345 | Superuser (accesso a /admin/) |

Oltre ai due ruoli dell'applicazione (Listener e Curator), è incluso un account **superuser** (`admin_demo`): è un Curator che inoltre ha accesso, tramite il pulsante **"Gestione"** nella barra laterale, al pannello di amministrazione di Django (indirizzo `/admin/`).

Per eseguire il progetto in locale: clonare il repository, creare e attivare un virtual environment, installare le dipendenze da `requirements.txt`, applicare le migrazioni e avviare il server.

```bash
git clone https://github.com/gaiabaldanzi-unifi/musicstream.git
cd musicstream
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Quando un utente tenta un'azione per cui non ha i permessi (ad esempio raggiungendo direttamente l'indirizzo di una pagina riservata), l'applicazione lo reindirizza e mostra un messaggio di errore come banner in cima alla pagina. Lo si può verificare dal browser così:

1. Accedere come `curator_demo` (Curator): aprire una canzone per vederne i dettagli e il testo, aggiungere una nuova canzone (dal pulsante "Aggiungi canzone") e creare una playlist.
2. Fare logout e accedere come `user_demo` (Listener): il pulsante "Aggiungi canzone" non è più visibile, perché il Listener non ha quel permesso.
3. Da Listener, raggiungere direttamente l'indirizzo di una pagina riservata, ad esempio `http://127.0.0.1:8000/canzoni/aggiungi/` (in locale) oppure `https://musicstream-iuvd.onrender.com/canzoni/aggiungi/` (online): l'applicazione reindirizza alla lista delle canzoni e mostra il messaggio "Solo i Curator possono aggiungere canzoni".

## Tecnologie

- Python 3.9 / Django 4.2
- Database SQLite (`db.sqlite3`, incluso e pre-popolato)
- Bootstrap 5 + Bootstrap Icons
- Tom Select (menu a tendina ricercabili)
- Gunicorn + WhiteNoise (esecuzione e file statici in produzione)

## Struttura del progetto

```
musicstream/
    accounts/         app per utenti, autenticazione e profili
    catalog/          app per canzoni, artisti, album, generi, playlist
    templates/        template HTML
    media/            file caricati dagli utenti (cover, avatar)
    db.sqlite3        database SQLite pre-popolato
    requirements.txt  dipendenze Python
    build.sh          script di build per il deploy
    manage.py         strumento di gestione di Django
```
