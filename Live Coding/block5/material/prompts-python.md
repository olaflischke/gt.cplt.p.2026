# Prompt-Vorlagen: Migration und Modernisierung (Python)

## Bestandscode verstehen

> Erkläre den markierten Code. Nenne die verwendete Python-Version, soweit
> erkennbar, sowie alle Standardbibliotheks- und Drittbibliotheks-APIs, von denen
> der Code abhängt. Ändere noch keinen Code.

## Veraltete APIs und Muster identifizieren

> Liste alle Stellen auf, die von der Migration auf eine aktuelle Python-Version
> betroffen sein könnten. Berücksichtige entfernte Stdlib-Module, veraltete
> Aliase und die verwendete Pydantic-Version. Ordne jeder Stelle zu, ob es sich um
> eine entfernte API, eine geänderte Standardeinstellung oder ein geändertes
> Verhalten handelt. Schlage noch keine Änderung vor.

## Risiko bewerten

> Bewerte für jede gefundene Stelle das Risiko einer Migration: gering, mittel
> oder hoch. Begründe die Einschätzung anhand von Testabdeckung, Kopplung an
> andere Komponenten und möglichen Verhaltensänderungen, insbesondere bei
> Validierungsregeln.

## Migrationsplan erzeugen

> Erstelle einen Migrationsplan vom alten Projektstand zum aktuellen Stand in
> kleinen, einzeln testbaren Schritten. Nenne zu jedem Schritt das Ziel, betroffene
> Dateien, Risiken und die Prüfung danach. Ändere noch keinen Code.

## Einen Schritt umsetzen

> Setze ausschließlich Schritt 1 des Migrationsplans um. Zeige den Diff. Erkläre,
> ob diese Änderung rein syntaktisch ist oder das Verhalten beeinflussen könnte.
> Halte dich an die vorhandenen Projektkonventionen.

## Verhalten vergleichen

> Vergleiche das Verhalten des migrierten Codes mit dem Original anhand der
> vorhandenen oder neu erstellten Tests. Nenne jede Abweichung ausdrücklich, auch
> wenn sie beabsichtigt erscheint.

## Pydantic-spezifische Prüfung

> Prüfe, ob die migrierte Pydantic-v2-Validierung bei denselben Eingaben zu
> denselben Ergebnissen führt wie die ursprüngliche Pydantic-v1-Validierung.
> Weise ausdrücklich auf Fälle hin, in denen die striktere Typprüfung von
> Pydantic v2 eine zuvor akzeptierte Eingabe jetzt ablehnen würde.

## Packaging-Migration prüfen

> Nenne alle Unterschiede zwischen der alten Konfiguration (`setup.py`,
> `requirements.txt`) und der neuen `pyproject.toml`. Prüfe insbesondere, ob alle
> Abhängigkeiten, Versionsgrenzen und Build-Einstellungen vollständig übernommen wurden.

## Ablehnen und zurücksetzen

> Setze die letzte Änderung zurück. Erkläre kurz, welches Verhalten sich
> verändert hätte oder warum der Schritt nicht auf den angeforderten Umfang
> begrenzt war.
