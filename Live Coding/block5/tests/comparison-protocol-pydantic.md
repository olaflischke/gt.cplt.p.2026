# Vergleichsprotokoll: Pydantic v1-Stil und Pydantic-v2-Stil

Da in einer einzelnen Python-Umgebung üblicherweise nur eine Pydantic-Hauptversion
installiert ist, lassen sich beide Varianten nicht automatisiert im selben Lauf
gegeneinander testen. Der Vergleich erfolgt deshalb anhand dieses Protokolls,
ergänzt durch getrennte Tests für die Pydantic-v1- und Pydantic-v2-Fassung.

Die v1-Charakterisierungstests wurden mit Pydantic 1.10.26 unter Python 3.14.6
ausgeführt. Der Projekt-Pin Pydantic 1.10.7 ließ sich in dieser Umgebung zwar
installieren, beim Definieren des Modells trat jedoch ein `ConfigError` zu den
Validator-Feldern auf. Die Ergebnisse sind daher noch nicht mit exakt dem
Projekt-Pin verifiziert.

Nach Schritt 3 wurde das unveränderte Legacy-Modell zusätzlich mit Pydantic
2.14.4 unter Python 3.14.6 ausgeführt. Die Ergebnisse sind im Abschnitt
„Beobachtung nach Schritt 3“ festgehalten. Die v1-Charakterisierungstests müssen
weiterhin in einer separaten v1-Umgebung ausgeführt werden.

## Zu vergleichende Fälle

1. **Gültiges Profil:** Benutzername mit Leerzeichen, positives Alter, gültige
   E-Mail-Adresse mit "@". Erwartung in beiden Versionen: Objekt wird erstellt,
   Leerzeichen im Benutzernamen werden entfernt.
2. **Negatives Alter:** Erwartung in beiden Versionen: Validierungsfehler.
3. **E-Mail ohne "@":** Erwartung in beiden Versionen: Validierungsfehler.
4. **Zahl in einem String-Feld (z. B. `username=123`):**
   - In der getesteten Pydantic-v1-Version 1.10.26 wird die Zahl implizit in
     einen String umgewandelt und akzeptiert.
   - Pydantic v2: konvertiert Zahlen standardmässig nicht mehr automatisch in
     String-Felder und lehnt den Wert ab (siehe Test
     `test_number_to_string_coercion_is_no_longer_implicit`).
   - Diese Abweichung ist eine fachlich sichtbare Verhaltensänderung, keine
     rein syntaktische Anpassung. **Entscheidung:** Zahlen in String-Feldern
     werden abgelehnt; das Pydantic-v2-Standardverhalten wird übernommen.
5. **Fließkommazahl mit Nachkommaanteil in `age`:**
   - In der getesteten Pydantic-v1-Version 1.10.26 wird ein solcher Wert
     verlustbehaftet zu `int` konvertiert.
   - Pydantic v2 lehnt eine solche Konvertierung standardmässig ab.
   - **Entscheidung:** Nicht-ganzzahlige Fließkommawerte für `age` werden
     abgelehnt; das Pydantic-v2-Verhalten wird übernommen.

## Getroffene Validierungsentscheidungen (20.11.2026)

- `username=123`: ablehnen, wie Pydantic v2 standardmässig.
- `age=1.5`: ablehnen, statt Nachkommastellen zu verlieren.
- Das sind bewusst akzeptierte Änderungen des Validierungsverhaltens. Die
  Migration ist deshalb nicht rein syntaktisch.

## Beobachtung nach Schritt 3 (20.11.2026)

Mit Pydantic 2.14.4 und dem noch unveränderten `legacy/user_profile_v1_style.py`:

- Das Modell wird geladen, aber `@validator` und die klassenbasierte `Config`
  erzeugen Deprecation-Warnungen.
- `anystr_strip_whitespace` erzeugt eine Warnung wegen Umbenennung. Die
  unveränderte Konfiguration trimmt unter Pydantic v2 die Werte tatsächlich
  nicht: `username` und `email` behalten ihre Rand-Leerzeichen.
- `username=123` und `age=1.5` enden jeweils mit `ValidationError`.
- Damit ist das Zielverhalten „Strings trimmen“ im aktuellen Zwischenstand
  noch nicht erhalten. Die unten aufgeführten Erwartungen für die migrierte
  Fassung sind erst nach ihrer Implementierung und ihren Tests bestätigt.

## Verifikation nach Schritt 4

Die modernisierte Fassung in `code_examples/modernized/user_profile_v2_style.py`
wurde mit Pydantic 2.14.4 unter Python 3.14.6 geprüft:

- Umgebende Leerzeichen werden aus `username` und `email` entfernt.
- Negatives Alter, E-Mail ohne "@", numerisches `username` und
  nicht-ganzzahliges `age` werden mit `ValidationError` abgelehnt.
- `age=0` bleibt zulässig.
- Die gezielten Tests ergaben **8 bestanden, 1 übersprungen**. Übersprungen
  wurde die separate v1-Baseline, weil diese Umgebung Pydantic v2 verwendet.
- Python 3.15.1 war nicht verfügbar; das Ergebnis bestätigt daher noch keinen
  Test auf dem festgelegten Zielinterpreter.

## Empfohlene manuelle Prüfung

- Vor der Freigabe prüfen, ob Aufrufer Zahlen in String-Felder oder
  Fließkommawerte für `age` senden. Solche Eingaben werden nach der festgelegten
  Regel zu Validierungsfehlern.
- Die v1-Charakterisierungstests mit Pydantic 1.10.7 in einer kompatiblen
  Python-Umgebung erneut ausführen, um das Verhalten des festgelegten
  Projekt-Pins zu bestätigen.
