# Breaking-Changes-Checkliste (Python)

Diese Liste wird in Block 5 verwendet, um Copilot-Analysen und eigene Beobachtungen
bei der Migration vom alten zum aktuellen Python-Projektstand zu vergleichen.

- [ ] Zielversion von Python ist eindeutig benannt und mit dem Projektumfeld abgestimmt.
- [ ] Entfernte Stdlib-Module sind erfasst (z. B. `distutils`, entfernt in Python 3.12).
- [ ] Entfernte Aliase sind erfasst (z. B. `collections.Mapping`, entfernt in Python 3.10).
- [ ] Breaking Changes zentraler Drittbibliotheken sind erfasst (hier: Pydantic v1 zu v2).
- [ ] Veränderungen im Validierungsverhalten (z. B. striktere Typprüfung) sind geprüft.
- [ ] Projekt- und Abhängigkeitsformat (`pyproject.toml`) ist vollständig und konsistent.
- [ ] Build- und CI-Konfiguration ist an das neue Projektformat angepasst.
- [ ] Tests für kritische Validierungs- und Berechnungsfunktionen liegen vor der Migration vor.
- [ ] Jeder Migrationsschritt ist einzeln nachvollziehbar und klein genug für ein Review.

## Sprachspezifische Ergänzungen: Python

- [ ] Verwendung von `distutils` statt `packaging`
- [ ] Verwendung veralteter `collections.*`-Aliase statt `collections.abc.*`
- [ ] Pydantic-v1-Muster (`@validator`, `class Config`) statt Pydantic-v2-Muster (`@field_validator`, `ConfigDict`)
- [ ] `setup.py`/`requirements.txt` statt `pyproject.toml`
- [ ] Fehlende `python_requires`/`requires-python`-Angabe für die Zielversion
