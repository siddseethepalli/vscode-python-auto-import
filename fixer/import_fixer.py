import ast
from collections.abc import Iterable
import pickle
import re
import subprocess
from typing import Counter, cast


class ImportFixer:
    index: dict[str, Counter[tuple[str | None, str]]]

    def __init__(self, index_path: str):
        with open(index_path, "rb") as f:
            self.index = cast(
                dict[str, Counter[tuple[str | None, str]]], pickle.load(f)
            )

    def get_fixed_contents(self, file_path: str) -> str:
        with open(file_path) as f:
            contents = f.read()

        missing_imports = self._get_missing_imports(file_path)
        if not missing_imports:
            return contents

        suggestions = self._get_suggestions(missing_imports)
        if not suggestions:
            return contents

        contents_plus_imports = self._apply_suggestions(contents, suggestions)

        return contents_plus_imports

    def _get_missing_imports(self, file_path: str) -> Iterable[str]:
        errors = (
            subprocess.check_output(
                f"flake8 --select F821 {file_path} || true", shell=True
            )
            .decode()
            .splitlines()
        )

        tokens: set[str] = set()
        for e in errors:
            match = re.search(r"[F821] undefined name '(.*)'", e)
            if match:
                tokens.add(match.group(1))

        return tokens

    def _get_suggestions(self, tokens: set[str]) -> dict[str, tuple[str | None, str]]:
        suggestions = {}
        for token in tokens:
            counts = self.index.get(token)
            if not counts:
                continue

            guess, _ = counts.most_common(1)[0]
            suggestions[token] = guess

        return suggestions

    def _apply_suggestions(
        self, contents: str, suggestions: dict[str, tuple[str | None, str]]
    ):
        # Decide which line to insert the imports on
        tree = ast.parse(contents)
        start_line = 0

        for element in tree.body:
            # Check for docstrings
            if type(element) == ast.Expr and type(element.value) == ast.Constant:
                start_line = element.lineno
                continue

            # Check for __team__
            if type(element) == ast.Assign and element.targets[0].id == "__team__":
                start_line = element.lineno
                continue

            break

        # Format the import statements
        imports: list[str] = []

        for name, (import_from, import_name) in suggestions.items():
            statement = ""

            if import_from:
                statement += f"from {import_from} "

            statement += f"import {import_name}"

            if name != import_name:
                statement += f" as {name}"

            imports.append(statement)

        # Insert the imports
        lines = contents.splitlines()
        lines_with_imports = lines[:start_line] + imports + lines[start_line:]

        return "\n".join(lines_with_imports).strip()
