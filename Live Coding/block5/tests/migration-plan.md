# Migrationsplan: Legacy-Beispiele auf Python 3.15 und Pydantic v2

## Annahmen und Ausgangslage

- Zielstand ist Python 3.15.1 und Pydantic 2.14.4.
- Die bestehende Paketdeklaration fordert Python `>=3.8` und pinnt Pydantic auf `1.10.7`. Für das Ziel Pydantic 2.14.4 wird die unterstützte Mindestversion bewusst auf Python `>=3.10` angehoben.
- Zahlen in String-Feldern und nicht-ganzzahlige Fließkommawerte für `age` werden abgelehnt. Diese Entscheidungen übernehmen das Pydantic-v2-Standardverhalten und sind fachliche Validierungsänderungen.
- Die Tests importieren `code_examples.modernized.*`, aber diese Module sind im derzeitigen Projektbestand nicht vorhanden.
- Eine `pyproject.toml` ist noch nicht vorhanden. Die Packaging-Migration ist daher ein eigener, separat prüfbarer Schritt.
- Der Plan umfasst die Pydantic- und Standardbibliotheksbeispiele im Legacy-Projekt. Er verändert den Code nicht.

## Schritte

| Schritt | Ziel | Betroffene Dateien | Risiko | Prüfung danach |
|---|---|---|---|---|
| 1. Zielversionen und Verhalten festlegen (**abgeschlossen**) | Ziel Python 3.15.1, Mindestversion Python 3.10 und Validierung der beiden Eingabegrenzfälle festlegen. | `tests/comparison-protocol-packaging.md`, `tests/comparison-protocol-pydantic.md` | **Entscheidung getroffen**: Die Python-Mindestversion wird angehoben; beide fraglichen Eingabeformen werden abgelehnt. Die verbleibende Auswirkung ist eine bewusst geänderte Kompatibilität bzw. Validierung. | In den Vergleichsprotokollen dokumentiert; Pydantic-Metadaten bestätigen `requires-python = ">=3.10"`. |
| 2. Pydantic-v1-Verhalten festhalten (**Tests erstellt; Pinprüfung offen**) | Vor der Migration die bisherigen Ergebnisse als Vergleichsbasis erfassen. | `tests/test_user_profile_v1_style.py`; `legacy/user_profile_v1_style.py` bleibt Vergleichsstand; `tests/comparison-protocol-pydantic.md`. | **Mittel**: 13 Tests bestehen mit Pydantic 1.10.26, aber der Projekt-Pin 1.10.7 scheitert beim Modellaufbau unter dem vorhandenen Python 3.14.6. | Die Baseline mit Pydantic 1.10.7 in einer kompatiblen Python-Umgebung erneut ausführen. |
| 3. Abhängigkeiten und Python-Metadaten aktualisieren (**Deklarationen geändert; Zielmatrixprüfung offen**) | Eine zum beschlossenen Python-Ziel passende Pydantic-Version festlegen und die deklarierte Python-Kompatibilität dazu passend halten. Auch `requests` und `packaging` auf Installierbarkeit prüfen. | `legacy/requirements.txt`, `legacy/setup.py`, `tests/comparison-protocol-packaging.md`, `tests/comparison-protocol-pydantic.md` | **Hoch im Zwischenstand**: Installation und Auflösung sind unter Python 3.14.6 erfolgreich, aber das unveränderte v1-Modell trimmt Strings nicht mehr und lehnt zuvor konvertierte Eingaben ab. Python 3.10 und 3.15.1 sind in der verfügbaren Umgebung nicht installiert. | Paketinstallation und Metadaten unter Python 3.14.6 geprüft; Laufzeitverhalten des unveränderten Modells mit Pydantic 2.14.4 protokolliert. Zielmatrixprüfung unter 3.10 und 3.15.1 bleibt offen. |
| 4. Pydantic-Modell migrieren (**implementiert; Zielinterpreterprüfung offen**) | Das v1-Modell in der von den vorhandenen Tests erwarteten modernisierten Struktur bereitstellen und dessen Validierung mit der festgelegten Pydantic-Version prüfen. | `code_examples/__init__.py`; `code_examples/modernized/__init__.py`; `code_examples/modernized/user_profile_v2_style.py`; `tests/test_user_profile_v2_style.py`; `tests/test_user_profile_v1_style.py`; `tests/comparison-protocol-pydantic.md` | **Mittel**: Die beschlossenen Abweichungen sind durch Tests abgedeckt. Python 3.15.1 ist in der verfügbaren Umgebung nicht installiert; die Zielmatrixprüfung bleibt offen. | `python -m pytest tests/test_user_profile_v2_style.py tests/test_user_profile_v1_style.py -q`: 8 bestanden, 1 v1-Testmodul übersprungen unter Python 3.14.6/Pydantic 2.14.4. |
| 5. Standardbibliotheksbeispiel modernisieren | Das Legacy-Beispiel unter Python 3.15 ausführbar machen und Versionsvergleich sowie Mapping-Prüfung testen. Die Semantik des Versionsvergleichs muss festgelegt sein, da ein anderer Parser andere Eingaben akzeptieren oder vergleichen kann. | Neue Datei `code_examples/modernized/stdlib_usage_modernized.py`; `tests/test_stdlib_usage_modernized.py`; `legacy/stdlib_usage_legacy.py` bleibt Vergleichsstand. | **Mittel bis hoch**: Der alte `distutils`-Import kann das Modul-Laden verhindern; `collections.Mapping` lässt die Funktion scheitern. Ein anderer Versionsparser kann das akzeptierte Format ändern. | `python -m unittest tests.test_stdlib_usage_modernized -v` ausführen; Fälle unterhalb, gleich und oberhalb der Mindestversion sowie gültige und ungültige Payloads prüfen. |
| 6. Packaging-Migration separat durchführen | Falls der Wechsel zu `pyproject.toml` zum Ziel gehört, Metadaten und Build-Konfiguration konsistent aus `setup.py` und `requirements.txt` übertragen. | Neue `pyproject.toml`; `legacy/setup.py`; `legacy/requirements.txt`; `tests/comparison-protocol-packaging.md` | **Mittel**: Abweichende Abhängigkeiten oder Python-Mindestversionen können eine Installation erlauben, die zur Laufzeit nicht funktioniert. Ein Wechsel des Build-Backends kann den Build beeinflussen. | Paket lokal bauen und installieren; Name, Version, Abhängigkeiten, `Requires-Python` und Build-Verhalten vergleichen. |
| 7. Gesamtprüfung auf dem Zielinterpreter | Code, Paketinstallation und Tests gemeinsam auf Python 3.15.1 prüfen. | Geänderte bzw. neue Dateien aus den Schritten 3–6 sowie alle Tests unter `tests/`. | **Mittel**: Einzeltests können funktionieren, während Paketimport oder Build scheitern. | `python -m unittest discover -s tests -v` ausführen; zusätzlich Paket-Build und Import aus der installierten Paketumgebung prüfen. |

## Ergebnis von Schritt 1

- Python-Zieltest: 3.15.1; unterstützte Mindestversion: 3.10.
- Pydantic-Ziel: 2.14.4.
- `username=123` und Fließkommawerte mit Nachkommaanteil für `age` werden
  abgelehnt.
- Diese Migration ist nicht rein syntaktisch: Die Validierung ändert sich
  sichtbar für zuvor gegebenenfalls akzeptierte Eingaben. Die Aufrufer müssen
  in den späteren Schritten auf solche Eingaben geprüft werden.

## Ergebnis von Schritt 3

- `legacy/requirements.txt` und `legacy/setup.py` pinnen nun Pydantic 2.14.4.
- `legacy/setup.py` deklariert nun Python `>=3.10`; `requests` und `packaging`
  behalten ihre bisherigen Versionsbereiche.
- Eine editable Installation und die Abhängigkeitsauflösung waren mit Python
  3.14.6 erfolgreich. Aufgelöst wurden Pydantic 2.14.4, Requests 2.34.2 und
  Packaging 26.3; die Paketmetadaten enthalten `Requires-Python >=3.10`.
- Beim unveränderten Legacy-Modell traten Deprecation-Warnungen für `@validator`
  und `Config` sowie eine Warnung für `anystr_strip_whitespace` auf. Die
  Stringwerte wurden nicht mehr getrimmt; numerisches `username` und
  nicht-ganzzahliges `age` wurden abgelehnt.
- Python 3.10 und 3.15.1 sind in der verfügbaren Umgebung nicht installiert;
  die dortige Installationsprüfung ist offen.
- Diese Änderung ist nicht rein syntaktisch: Die Python-Untergrenze schließt
  3.8 und 3.9 aus. Das Pydantic-Hauptversionsupdate kann ausserdem das
  Validierungsverhalten ändern; die beschlossenen Abweichungen sind im
  Pydantic-Vergleichsprotokoll dokumentiert.

## Ergebnis von Schritt 4

- Das Pydantic-v2-Modell verwendet `ConfigDict(str_strip_whitespace=True)` und
  `@field_validator`; die zuvor veralteten v1-Konstrukte sind nicht mehr nötig.
- `username` und `email` werden wieder getrimmt. Negatives Alter, E-Mail ohne
  "@", numerisches `username` und nicht-ganzzahliges `age` werden abgelehnt;
  Alter `0` bleibt zulässig.
- Die gezielten Tests ergaben unter Python 3.14.6 und Pydantic 2.14.4 **8
  bestanden, 1 übersprungen**. Die übersprungene v1-Baseline benötigt eine
  separate Pydantic-v1-Umgebung.
- Diese Änderung ist nicht rein syntaktisch: Trimmen wird als bisheriges
  Verhalten wiederhergestellt, während numerisches `username` und
  nicht-ganzzahliges `age` bewusst anders validiert werden als unter v1.
- Die Prüfung mit Python 3.15.1 bleibt offen, da dieser Interpreter nicht
  verfügbar war.
