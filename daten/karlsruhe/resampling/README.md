# Resampling von statistischen Daten auf Wahlbezirke

In ihrem [Transparenzportal](https://transparenz.karlsruhe.de) veröffentlicht
die Stadt Karlsruhe viele statistische Daten. Allerdings liegen diese dort nur
auf Stadtteil-Ebene vor, nicht heruntergerechnet auf Wahlbezirke. Wir haben
sie daher selbst entsprechend umgerechnet.

Diese Umrechnung ist allerdings nicht exakt, sondern eher als Schätzung zu
verstehen. Das genaue Vorgehen ist unten dokumentiert.


## Umgerechnete Statistiken

Die umgerechneten Statistiken findet Ihr in der Datei
[wahlbezirke.geojson](wahlbezirke.geojson).

Die folgenden Statistiken wurden umgerechnet. Wo nicht anders angegeben
beziehen sich die Daten auf das Jahr 2016.

### Allgemein

* `Einwohner_2016`: Anzahl der Einwohner mit Hauptwohnsitz
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerung/resource/041383f1-e003-4a91-9fd2-c19adb5434ee))

* `Zuzüge_2016`: Anzahl der zugezogenen Personen (Hauptwohnsitz)
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerungsbewegungen/resource/ed7db535-9245-4107-b522-5c95045d7073))

* `Wegzüge_2016`: Anzahl der weggezogenen Personen (Hauptwohnsitz)
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerungsbewegungen/resource/adf4edbf-bc42-4245-aebf-c3a5ce97ac82))

### Altersstruktur

* `Alter_0-19_2016`: Anzahl der Einwohner mit Hauptwohnsitz unter 20 Jahren
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/182784ed-dec2-4970-b6b6-f8f213188643))

* `Alter_20-64_2016`: Anzahl der Einwohner mit Hauptwohnsitz zwischen 20 und 59 Jahren
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/7e3b54d8-53a7-45b5-99e6-0ecbcf963647))

* `Alter_65+_2016`: Anzahl der Einwohner mit Hauptwohnsitz im Alter von 65 und älter
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/7e3b54d8-53a7-45b5-99e6-0ecbcf963647))

* `Geburten_2016`: Anzahl der Geburten
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerungsbewegungen/resource/272a56f5-8e7b-4e72-8d90-19ee6840db23))

* `Gestorbene_2016`: Anzahl der Sterbefälle
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerungsbewegungen/resource/0fcf19fd-28e0-4032-9341-b61dc41e38d5))

### Migration

* `DeutscheMitMigrationshintergrund_2016`: "Personen [mit Hauptwohnsitz], die eine deutsche Staatsangehörigkeit besitzen und gleichzeitig anhand der Eintragungen im Einwohnermelderegister einen persönlichen Migrationshintergrund erkennen lassen [...]. Hierzu werden auch (deutsche) Kinder- und Jugendliche mit einer Option auf die deutsche Staatsangehörigkeit gerechnet."
  ([Quelle](https://transparenz.karlsruhe.de/dataset/migration/resource/82656038-a0a3-4793-843b-1ebc89ba3fed))

* `AusländerInnen_2016`: Personen mit Hauptwohnsitz, die nicht die deutsche Staatsangehörigkeit besitzen
  ([Quelle](https://transparenz.karlsruhe.de/dataset/migration/resource/82656038-a0a3-4793-843b-1ebc89ba3fed))

### Bildung

* `AnteilÜbergängeGemeinschaftsschule_2016`: Quote der Übergänge von Schülern aus Grundschulen des jeweiligen *Stadtteils* auf Gemeinschaftsschulen
  ([Quelle](https://transparenz.karlsruhe.de/dataset/ubergange-auf-weiterfuhrende-schulen-ubergangsquoten/resource/0b7c2a18-8158-44f8-80e2-5da92d5e1deb))

* `AnteilÜbergängeHauptUndWerkrealschule_2016`: Quote der Übergänge von Schülern aus Grundschulen des jeweiligen *Stadtteils* auf Haupt- und Werksrealschulen
  ([Quelle](https://transparenz.karlsruhe.de/dataset/ubergange-auf-weiterfuhrende-schulen-ubergangsquoten/resource/79cfcef3-34ec-4c80-887d-895dd9d79327))

* `AnteilÜbergängeRealschule_2016`: Quote der Übergänge von Schülern aus Grundschulen des jeweiligen *Stadtteils* auf Realschulen
  ([Quelle](https://transparenz.karlsruhe.de/dataset/ubergange-auf-weiterfuhrende-schulen-ubergangsquoten/resource/38efcac4-1721-42ee-b4d4-a68853665f0f))

* `AnteilÜbergängeGymnasium_2016`: Quote der Übergänge von Schülern aus Grundschulen des jeweiligen *Stadtteils* auf Gymnasien
  ([Quelle](https://transparenz.karlsruhe.de/dataset/ubergange-auf-weiterfuhrende-schulen-ubergangsquoten/resource/b081e346-17c7-40f1-b874-68dde596bded))

* `AnteilÜbergängeSonstige_2016`: Quote der sonstigen Ab- und Übergänge von Schülern aus Grundschulen des jeweiligen *Stadtteils*, z.B. Wiederholer
  ([Quelle](https://transparenz.karlsruhe.de/dataset/ubergange-auf-weiterfuhrende-schulen-ubergangsquoten/resource/ebec5f95-ad83-42c0-82b5-87a208fd6543))


## Lizenz

Die Statistiken und Umrisse der Wahlbezirke stammen aus dem Transparenzportal
der Stadt Karlsruhe und stehen unter der Lizenz
[Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0).


## Details zur Umrechung

Für die Umrechnung von einer geografischen Einteilung (Stadtteile) in eine
andere (Wahlbezirke) kam die Software
[CoGran](https://github.com/berlinermorgenpost/cogran) zum Einsatz.


### Schritt 1: Einwohner pro Wahlbezirk schätzen

Die Anzahl der Einwohner eines Gebietes (wie z.B. eines Stadtteils) ist eine
wichtige Normierungsgröße um entsprechende Statistiken einordnen zu können.
Grundlage für die Schätzung der Einwohner pro Wahlbezirk waren die Einwohner
pro Stadtteil (aus dem Transparenzportal). Diese wurden, gewichtet nach der
Anzahl der Wahlbeteiligten pro Wahlbezirk (aus dem Transparenzportal) auf
die Wahlbezirke "verteilt".


### Schritt 2: Statistiken auf Wahlbezirke umrechnen

Im zweiten Schritt wurden die Statisiken auf Stadtteil-Ebene auf Wahlbezirke
umgerechnet. Jeder Wahlbezirk wurde dabei mit der in Schritt 1 geschätzen Zahl
seiner Einwohner gewichtet.

