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

* `Einwohner_2016`: Anzahl der Einwohner mit Hauptwohnsitz
  ([Quelle](https://transparenz.karlsruhe.de/dataset/bevolkerung/resource/041383f1-e003-4a91-9fd2-c19adb5434ee))

* `Alter_0-19_2016`: Anzahl der Einwohner mit Hauptwohnsitz unter 20 Jahren
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/182784ed-dec2-4970-b6b6-f8f213188643))

* `Alter_20-64_2016`: Anzahl der Einwohner mit Hauptwohnsitz zwischen 20 und 59 Jahren
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/7e3b54d8-53a7-45b5-99e6-0ecbcf963647))

* `Alter_65+_2016`: Anzahl der Einwohner mit Hauptwohnsitz im Alter von 65 und älter
  ([Quelle](https://transparenz.karlsruhe.de/dataset/altersstruktur/resource/7e3b54d8-53a7-45b5-99e6-0ecbcf963647))


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

