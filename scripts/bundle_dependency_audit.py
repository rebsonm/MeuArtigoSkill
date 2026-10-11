"""Static closure checks for an installable Meu Artigo Skill archive.

The package may contain offline optional Python modules; not all external
Python libraries are required at installation. We only check that *local*
Python imports, and the root SKILL's Markdown navigation, are present.
This is an engineering contract, not an authenticity signature.
"""
from __future__ import annotations

import ast
import re
from pathlib import PurePosixPath

LINK = re.compile(r"\]\(([^)\n]+)\)")


def audit(members: dict[str, bytes], *, local_source_modules: set[str] | None = None) -> dict:
    errors = []
    names = set(members)
    installed = {
        PurePosixPath(filename).stem for filename in names
        if filename.startswith("scripts/") and filename.endswith(".py")
        and len(PurePosixPath(filename).parts) == 2
    }
    known = installed | (local_source_modules or set())
    root = members.get("SKILL.md")
    if root is None:
        errors.append("MISSING_SKILL_ENTRYPOINT")
    else:
        try:
            markdown = root.decode("utf-8")
        except UnicodeError:
            errors.append("UNREADABLE_SKILL_ENTRYPOINT")
        else:
            for reference in LINK.findall(markdown):
                path = reference.strip().split(" ", 1)[0].strip("<>")
                if not path or path.startswith(("#", "https://", "http://", "mailto:")):
                    continue
                candidate = path.split("#", 1)[0].split("?", 1)[0]
                normalized = PurePosixPath(candidate)
                if (normalized.is_absolute() or ".." in normalized.parts
                        or candidate not in names):
                    errors.append("MISSING_OR_UNSAFE_ENTRYPOINT_LINK:" + candidate)
    for filename in sorted(names):
        if not filename.startswith("scripts/") or not filename.endswith(".py"):
            continue
        try:
            tree = ast.parse(members[filename].decode("utf-8"), filename=filename)
        except (UnicodeError, SyntaxError):
            errors.append("INVALID_INSTALLED_PYTHON:" + filename)
            continue
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".", 1)[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level and not node.module:
                    errors.append("UNRESOLVED_RELATIVE_IMPORT:" + filename)
                    continue
                if node.level:
                    # The Skill ships a scripts directory, not a Python package
                    # with a namespace for relative intra-script imports.
                    errors.append("RELATIVE_IMPORT_UNSUPPORTED:" + filename)
                    continue
                modules = [node.module.split(".", 1)[0]] if node.module else []
            for module in modules:
                if module in known and module not in installed:
                    errors.append("MISSING_LOCAL_PYTHON_DEPENDENCY:"
                                  + filename + "->" + module)
    return {"errors": sorted(set(errors)), "installed_script_modules": len(installed),
            "checked_markdown_entrypoint": root is not None,
            "external_optional_packages_independently_tested": False,
            "scientific_quality_validated": False}
