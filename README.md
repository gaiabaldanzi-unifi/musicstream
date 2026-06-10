# MusicStream

Progetto universitario per l'esame di Progettazione e Produzione Multimediale.
Servizio di streaming musicale sviluppato con Django (Track 4 — Full-Stack Web Application).

---

## Funzionalità

- Catalogo di canzoni, artisti, album e generi musicali
- Ricerca globale per testo e categoria
- Due ruoli utente: **Listener** e **Curator**
  - Il Curator può aggiungere, modificare ed eliminare canzoni, artisti, album e generi
  - Il Listener può creare e gestire le proprie playlist
- Gestione playlist personalizzate con cover, descrizione e durata totale calcolata
- Profilo utente modificabile con avatar
- Autenticazione completa (registrazione, login, logout)

---

## Tecnologie

- Python 3.9
- Django 4.2
- SQLite (sviluppo)
- Bootstrap 5 + Bootstrap Icons
- Tom Select (dropdown ricercabili)

---

## Installazione locale

```bash
# 1. Clona il repository
git clone <url-repo>
cd musicstream

# 2. Crea e attiva il virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Applica le migrazioni
python manage.py migrate

# 5. (Opzionale) Popola il database con dati di esempio
python populate_db.py

# 6. Avvia il server
python manage.py runserver
```

Apri il browser su `http://127.0.0.1:8000`

---

## Account di test

| Username | Password | Ruolo |
|---|---|---|
| curator1 | demo1234! | Curator |
| listener1 | demo1234! | Listener |

---

## Struttura del progetto

```
musicstream/
    accounts/       → app per utenti, autenticazione e profili
    catalog/        → app per canzoni, artisti, album, generi, playlist
    templates/      → template HTML
    media/          → file caricati dagli utenti
    requirements.txt
    manage.py
```

---

## Autore

Gaia Baldanzi — A.A. 2025/2026
