# Vergleichsprotokoll: Packaging-Migration (setup.py/requirements.txt zu pyproject.toml)

## Zu vergleichende Aspekte

1. **Projektname und Version:** Stimmen name/version in setup.py und
   pyproject.toml überein?
2. **Abhängigkeiten:** Sind alle Einträge aus requirements.txt vollständig
   und mit denselben Versionsgrenzen in dependencies von pyproject.toml
   übernommen worden?
3. **Python-Zielversion:** Als Ziel gilt Python 3.15.1; die unterstützte
   Mindestversion wird auf `>=3.10` festgelegt. Das entspricht der
   `requires-python`-Angabe von Pydantic 2.14.4. Die bisherige Angabe
   `python_requires=">=3.8"` wird damit bewusst angehoben.
4. **Build-Backend:** Ist ein [build-system]-Abschnitt vorhanden und konsistent
   mit dem bisher verwendeten Build-Werkzeug?
5. **Tool-Konfiguration:** Wurden Einstellungen für Testwerkzeuge, Linter oder
   Typprüfung, die bisher in separaten Dateien lagen, nach pyproject.toml
   übernommen, falls dies im Projekt gewünscht ist?

## Empfohlene manuelle Prüfung

- Das neue Projektformat mit dem im Unternehmen etablierten Installationsschritt
  (z. B. ein editierbares/lokales Setup) testweise aufbauen und auf Fehler prüfen.
- Build- und CI-Pipeline mit dem neuen Projektformat testen.
- Sicherstellen, dass keine Abhängigkeit beim Wechsel versehentlich entfernt wurde.

## Getroffene Entscheidung (20.11.2026)

- Zieltestversion: Python 3.15.1.
- Unterstützte Mindestversion: Python 3.10.
- Begründung: Pydantic 2.14.4 deklariert `requires-python = ">=3.10"`.
- Die Anhebung der Mindestversion ist eine Kompatibilitäts- und
  Packaging-Änderung, keine rein syntaktische Quellcodeänderung.

## Ergebnis der Abhängigkeitsprüfung

- `legacy/setup.py` und `legacy/requirements.txt` deklarieren Pydantic 2.14.4;
  `python_requires` ist auf `>=3.10` angehoben.
- `requests` und `packaging` behalten ihre bisherigen Versionsbereiche.
- Die editable Installation und Abhängigkeitsauflösung waren mit Python 3.14.6
  erfolgreich. Aufgelöst wurden Requests 2.34.2 und Packaging 26.3.
- Python 3.10 und 3.15.1 standen in der Prüfungsumgebung nicht zur Verfügung;
  diese Installationsprüfungen bleiben offen.
