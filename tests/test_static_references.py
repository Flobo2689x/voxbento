"""Every static file a template links to must exist, or each page view logs a 404."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent / "portal"
STATIC_REF = re.compile(r"url_for\(\s*['\"]static['\"]\s*,\s*path\s*=\s*['\"]([^'\"]+)['\"]")


def _static_references():
    for template in sorted((ROOT / "templates").rglob("*.html")):
        for match in STATIC_REF.finditer(template.read_text(encoding="utf-8")):
            yield pytest.param(template.relative_to(ROOT).as_posix(), match.group(1), id=match.group(1))


@pytest.mark.parametrize(("template", "path"), list(_static_references()))
def test_template_static_reference_exists(template, path):
    assert (ROOT / "static" / path).is_file(), f"{template} links to missing static file {path}"
