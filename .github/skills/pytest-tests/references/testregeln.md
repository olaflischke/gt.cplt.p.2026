# Testregeln

- Testfunktionen heißen test_funktion_szenario_erwartetesErgebnis.
- Jeder Test folgt dem AAA-Muster (Arrange, Act, Assert). Die Abschnitte trennst du mit Leerzeilen.
- Mehrere Eingaben für dieselbe Prüfung: @pytest.mark.parametrize.
- Mindestens ein Test für Grenzwerte: 0, leer, None, maximaler Wert.
- Abhängigkeiten mit unittest.mock.Mock oder pytest-mock ersetzen. Keine echte Datenbank.
- Gemeinsame Testdaten als Fixture in conftest.py.