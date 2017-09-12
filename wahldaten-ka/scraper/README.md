# Scraper für Karlsruher Wahldaten

Das Wahlamt der Stadt Karlsruhe veröffentlicht die Ergebnisse zur
Bundestagswahl live auf seiner [Webseite](https://www.karlsruhe.de/b4/buergerengagement/wahlen.de).
Dieser Scraper extrahiert die Daten von dort und exportiert sie in
maschinenlesbare Formate (CSV und JSON).


## Installation

Der Scraper benötigt Python 2.7 oder Python 3.3 und später. Die
Abhängigkeiten installiert Ihr am besten in ein `virtualenv`:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


## Daten scrapen

Stellt sicher dass Euer `virtualenv` aktiviert ist:

    source venv/bin/activate

Dann startet Ihr den Scraper wie folgt:

    python ka_wahldaten_scraper.py

Der Scraper schreibt die 2 Dateien `results.csv` und `results.json` ins
aktuelle Verzeichnis.


## Konfiguration

Bis die Webseite mit den Ergebnissen für die BTW 2017 online sind nutzt der
Scraper stattdessen die Seiten für die BTW 2013. Die entsprechenden URLs sind
fest eincodiert und müssen nicht konfiguriert werden.

