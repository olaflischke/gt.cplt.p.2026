Ich prüfe den vorhandenen Projektaufbau, die Paketmetadaten und Tests, damit der Plan auf tatsächlich vorhandenen Dateien und überprüfbaren Zwischenschritten basiert.

Find files matching `**/*`

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\legacy\\user_profile_v1_style.py"
}

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\legacy\\setup.py"
}

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\legacy\\requirements.txt"
}

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\tests\\test_user_profile_v2_style.py"
}

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\tests\\test_stdlib_usage_modernized.py"
}

Search for `pytest|unittest|python_requires|requires-python|pydantic|standard|modernized|...`

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\tests\\comparison-protocol-pydantic.md"
}

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\tests\\comparison-protocol-packaging.md"
}

Find files matching `**/{user_profile_v2_style.py,stdlib_usage_modernized.py,pyproject.toml}`

Read 
Completed with input: {
  "path": "C:\\training\\gt.cplt.p.2026\\Live Coding\\block5\\legacy\\stdlib_usage_legacy.py"
}

## Annahmen und Ausgangslage

Ich setze „aktuell“ mit **Python 3.15.1** und **Pydantic 2.14.4** an. Pydantic 2.14.4 führt Unterstützung für Python 3.15 auf ([Python 3.15.1](https://www.python.org/downloads/release/python-3151/), [Pydantic 2.14.4](https://github.com/pydantic/pydantic/releases/tag/v2.14.4)).

Im Projekt gibt es bereits Tests, die `code_examples.modernized...` importieren, aber im geprüften Projektbestand fehlen diese Module. Auch eine `pyproject.toml` ist nicht vorhanden. Außerdem ist noch zu entscheiden, ob nur Python 3.15 geprüft oder die bisher deklarierte Unterstützung ab Python 3.8 beibehalten werden soll. Letzteres beeinflusst die mögliche Pydantic-Version.

## Migrationsplan

| Schritt | Ziel | Betroffene Dateien | Risiko | Prüfung danach |
|---|---|---|---|---|
| **1. Zielversionen und Validierungsverhalten festlegen** | Python-Ziel und unterstützte Mindestversion klären. Fachlich entscheiden, wie Eingaben wie `username=123` oder ein Fließkommawert für `age` behandelt werden sollen. | `comparison-protocol-packaging.md`, `comparison-protocol-pydantic.md` | **Hoch**, solange Mindestversion und Validierungsvertrag offen sind: die Pydantic-Version kann die unterstützten Python-Versionen begrenzen, und Eingaben können sich anders verhalten. | Entscheidungsmatrix dokumentieren: Python-Version(en), Pydantic-Version und erwartete Ergebnisse für die Randfälle. |
| **2. Verhalten von Pydantic v1 festhalten** | Vor der Migration die bisherigen Ergebnisse als Vergleichsbasis erfassen, damit Änderungen an der Eingabevalidierung sichtbar werden. | Neue Tests, z. B. `tests/test_user_profile_v1_style.py`; `user_profile_v1_style.py` bleibt Vergleichsstand. | **Mittel**: Im Bestand gibt es keinen direkten Test für das Legacy-Modell. Die Baseline muss mit einer Umgebung laufen, in der die alte Abhängigkeit funktioniert. | Fälle für Whitespace, negatives Alter, ungültige E-Mail, Zahl in String-Feld und Fließkommawert für `age` mit Pydantic v1 ausführen und Ergebnisse festhalten. |
| **3. Abhängigkeiten und Python-Metadaten aktualisieren** | Eine für das beschlossene Python-Ziel geeignete Pydantic-Version festlegen und die deklarierte Python-Kompatibilität dazu passend halten. Dabei auch `requests` und `packaging` auflösbar und installierbar halten. | `requirements.txt`, `setup.py` | **Hoch**, falls die deklarierte Mindestversion und die tatsächlich unterstützten Abhängigkeiten auseinanderlaufen oder die aufgelösten Pakete keine Python-3.15-kompatiblen Distributionen bereitstellen. | Abhängigkeiten in einer sauberen Python-3.15.1-Umgebung auflösen und installieren; Paketimport sowie Metadaten prüfen. Bei beibehaltener älterer Python-Unterstützung zusätzlich gegen deren Mindestversion testen. |
| **4. Pydantic-Modell migrieren** | Das v1-Modell in der vom bestehenden Test erwarteten modernisierten Struktur bereitstellen und seine Validierung mit der festgelegten Pydantic-Version prüfen. Die bestehende Geschäftslogik – Whitespace-Behandlung, Altersprüfung und E-Mail-Prüfung – getrennt von Änderungen der Typkonvertierung verifizieren. | Neue Datei `code_examples/modernized/user_profile_v2_style.py`; `test_user_profile_v2_style.py`; gegebenenfalls `comparison-protocol-pydantic.md` | **Hoch** für unklare Eingaben: Pydantic v2 kann zuvor akzeptierte Werte zurückweisen. Das vorhandene Testmodul prüft einige Fälle, aber nicht direkt die derzeit fehlende modernisierte Implementierung oder alle Typgrenzen. | `python -m unittest tests.test_user_profile_v2_style -v`; zusätzlich die in Schritt 1 festgelegten Whitespace-, Zahlen- und Altersgrenzen gegen die v1-Baseline vergleichen. |
| **5. Standardbibliotheksbeispiel modernisieren** | Das Legacy-Beispiel unter Python 3.15 ausführbar machen und Versionsvergleich sowie Mapping-Prüfung gezielt testen. Dabei sicherstellen, dass die Semantik des Versionsvergleichs festgelegt ist, da ein anderer Parser andere Eingaben akzeptieren oder vergleichen kann. | Neue Datei `code_examples/modernized/stdlib_usage_modernized.py`; `test_stdlib_usage_modernized.py`; `stdlib_usage_legacy.py` bleibt Vergleichsstand. | **Mittel bis hoch**: Der alte `distutils`-Import kann das Laden des Moduls verhindern; `collections.Mapping` lässt die Funktion scheitern. Ein Ersatz für `LooseVersion` kann außerdem das akzeptierte Versionsformat verändern. | `python -m unittest tests.test_stdlib_usage_modernized -v`; Fälle unterhalb, gleich und oberhalb der Mindestversion sowie gültige und ungültige Payloads prüfen. |
| **6. Packaging-Migration separat durchführen** | Falls der Wechsel zu `pyproject.toml` Teil des Ziels ist, Metadaten und Build-Konfiguration von `setup.py`/`requirements.txt` konsistent übertragen. Das ist von der Python-Laufzeitmigration getrennt prüfbar. | Neue `pyproject.toml`; `setup.py`, `requirements.txt`, `comparison-protocol-packaging.md` | **Mittel**: Abweichende Abhängigkeiten oder Python-Mindestversionen können eine Installation erlauben, die zur Laufzeit nicht funktioniert. Ein Wechsel des Build-Backends kann zusätzlich den Build beeinflussen. | Paket lokal bauen und installieren; Name, Version, Abhängigkeiten, `Requires-Python` und Build-Verhalten mit dem bisherigen Paket vergleichen. |
| **7. Gesamtprüfung auf dem Zielinterpreter** | Sicherstellen, dass Code, Paketinstallation und Tests gemeinsam auf Python 3.15.1 funktionieren. | Geänderte bzw. neue Dateien aus den Schritten 3–6 sowie alle Tests unter `tests/`. | **Mittel**: Einzeltests können funktionieren, während Paketimport oder Build scheitern; deshalb beides getrennt prüfen. | Gesamte Testsuite mit `python -m unittest discover -s tests -v` ausführen und zusätzlich den Paket-Build sowie einen Import aus der installierten Paketumgebung prüfen. |

Der kritischste fachliche Freigabepunkt ist Schritt 1: Vor Abschluss der Pydantic-Migration muss klar sein, ob Änderungen bei Eingaben wie Zahlen in String-Feldern akzeptabel sind. **Es wurde kein Code geändert.**