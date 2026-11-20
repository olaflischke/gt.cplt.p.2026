# -*- coding: utf-8 -*-
"""Legacy-Beispiel: veraltete Standardbibliothek-Nutzung.

distutils wurde in Python 3.12 aus der Standardbibliothek entfernt.
collections.Mapping wurde als Alias in Python 3.10 entfernt.
"""

from distutils.version import LooseVersion
import collections


def is_supported_version(version_string):
    minimum = LooseVersion("1.2.0")
    return LooseVersion(version_string) >= minimum


def validate_payload(payload):
    # collections.Mapping ist ein entferntes Alias für collections.abc.Mapping.
    if not isinstance(payload, collections.Mapping):
        raise TypeError("payload must be a mapping")
    return True
