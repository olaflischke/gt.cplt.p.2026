# Code-Smells-Checkliste (Python)

Diese Liste wird in Block 4 verwendet, um Copilot-Analysen und eigene Beobachtungen
zu vergleichen.

- [ ] Lange Funktion/Methode mit mehreren Verantwortlichkeiten
- [ ] Tiefe Verschachtelung von Bedingungen oder Schleifen
- [ ] Magic Numbers oder Magic Strings ohne erklaerenden Namen
- [ ] Doppelter Code fuer dieselbe fachliche Regel
- [ ] Unklare, abgekuerzte oder irrefuehrende Namen
- [ ] Fehlende oder stillschweigend ignorierte Fehlerbehandlung
- [ ] Vermischte Verantwortlichkeiten (Validierung, Berechnung, Ein-/Ausgabe)
- [ ] Hohe Anzahl unabhaengiger Entscheidungswege (hohe Komplexitaet)
- [ ] Implizite Abhaengigkeit von Reihenfolge oder globalem Zustand
- [ ] Fehlendes oder unzureichendes Testnetz vor der Aenderung

## Sprachspezifische Ergaenzungen: Python

- [ ] Fehlende Typannotationen an zentralen Schnittstellen
- [ ] Verwendung von veraenderlichen Standardargumenten (`def f(x, cache={})`)
- [ ] Breite `except Exception`-Bloecke ohne differenzierte Behandlung

