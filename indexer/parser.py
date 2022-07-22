import ast

from utils import change_directory, list_all_target_files


class ParsedImport:
    def __init__(
        self,
        module,
        import_name,
        import_alias,
        import_from,
    ):
        self.module = module
        self.import_name = import_name
        self.import_alias = import_alias
        self.import_from = import_from

    @property
    def name(self):
        return self.import_alias or self.import_name


def parse_all_project_imports(base_dir: str):
    results = []

    with change_directory(base_dir):
        targets = list_all_target_files()
        for target in targets:
            try:
                results.extend(parse_imports_from_path(target))
            except Exception:
                pass

    return results


def parse_imports_from_path(path):
    module = path.replace("./", "").replace(".py", "").replace("/", ".")
    parser = ImportParser(module)

    with open(path, "r") as f:
        tree = ast.parse(f.read())
    parser.visit(tree)

    return parser.parsed_imports


class ImportParser(ast.NodeVisitor):
    def __init__(self, module: str):
        self.module = module
        self.parsed_imports = []

    def visit_Import(self, node):
        for name in node.names:
            self.parsed_imports.append(
                ParsedImport(
                    module=self.module,
                    import_name=name.name,
                    import_alias=name.asname,
                    import_from=None,
                )
            )

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.level == 0:
            import_from = node.module
        else:
            import_from = ".".join(self.module.split(".")[: -node.level])
            if node.module:
                import_from += "." + node.module

        for name in node.names:
            self.parsed_imports.append(
                ParsedImport(
                    module=self.module,
                    import_name=name.name,
                    import_alias=name.asname,
                    import_from=import_from,
                )
            )

        self.generic_visit(node)
