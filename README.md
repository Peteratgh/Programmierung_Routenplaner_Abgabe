# Routenplaner README  


## Nutzung  
Dieses Programm ermöglicht es Benutzern, die schnellste oder kürzeste Route zwischen den Städten Höxter und Rostock zu finden. Die verfügbaren Fortbewegungsmittel sind zu Fuß (ped), Fahrrad (bic) und Auto (car). Das Programm kann jederzeit durch die Eingabe "exit" beendet werden.

### Hinweis

Bei der Zeitberechnung für den Fußgänger wird eine Geschwindigkeit von 5 km/h angekommen. Bei der Streckenberechnung mit dem Auto werden außerdem Einbahnstraßen berücksichtigt.

## Anwendung  
* Starte das Programm.  
* Gib die gewünschte Stadt ein.  
* Wähle das Fortbewegungsmittel (ped/bic/car).  
* Wähle zwischen der schnellsten Route (time) oder der kürzesten Route (distance).  
* Gib den Startpunkt und das Ziel ein.  
* Die berechnete Route, Distanz, Fahrzeit und die Abfolge der befahrenen Straßen werden angezeigt.  
* Die Route kann als KML-Datei exportiert werden.
* Wähle, ob du das Programm erneut ausführen möchtest.

### To-Do
- [x] Export von KML optional machen
- [x] Die auswahl des Startknotens soll nicht anhand des ersten Eintrags der txt file statt finden sondern anhand des mittleren Eintrags
- [x] Abgefahrene Straßen übersichtlicher ausgeben(mit Teilstreckendistanz)
- [x] Richtungen hinzufügen
- [ ] logging implementieren
- [x] Gesamtzeit für die Ausführung des Programms ausgeben


## Autoren
Peter Schleining
