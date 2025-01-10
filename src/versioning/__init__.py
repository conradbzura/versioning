from __future__ import annotations

import pkg_resources

from versioning._version import PythonicVersion, parser, SemanticVersion

__all__ = ["PythonicVersion", "parser", "SemanticVersion"]

for entry_point in pkg_resources.iter_entry_points("versioning.plugins"):
    entry_point.load()
