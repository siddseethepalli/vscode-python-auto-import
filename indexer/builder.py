from collections import Counter, defaultdict
from datetime import timedelta
import hashlib
import os
from pathlib import Path
import pickle
import time

from parser import parse_all_project_imports
from utils import get_base_dir

INDEX_ROOT = Path.home() / ".cache" / "python-auto-importer"
INDEX_TTL = timedelta(days=1)


class IndexBuilder:
    def get_index_path(self, file_path: str) -> str:
        base_dir = get_base_dir(file_path)
        if not base_dir:
            raise Exception(f"Could not find base directory for file: {file_path}")

        index_name = hashlib.sha256(base_dir.encode("utf-8")).hexdigest()
        index_path = INDEX_ROOT / index_name

        index_exists = index_path.exists()

        if index_exists:
            last_modified = index_path.stat().st_mtime
            if time.time() - last_modified < INDEX_TTL.total_seconds():
                return str(index_path)

        if not index_exists:
            os.makedirs(INDEX_ROOT, exist_ok=True)

        index = self._create_index_in_memory(base_dir)

        with open(index_path, "wb") as f:
            pickle.dump(index, f)

        return str(index_path)

    def _create_index_in_memory(
        self, base_dir: str
    ) -> dict[str, Counter[tuple[str | None, str]]]:
        parsed_imports = parse_all_project_imports(base_dir)

        grouped = defaultdict(list)
        for p in parsed_imports:
            grouped[p.name].append(p)

        return {
            name: Counter((i.import_from, i.import_name) for i in imports)
            for name, imports in grouped.items()
        }
