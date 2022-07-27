import argparse

from import_fixer import ImportFixer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("--index-path", dest="index_path", required=True)

    args = parser.parse_args()
    file_path = args.file_path
    index_path = args.index_path

    fixer = ImportFixer(index_path)
    fixed_contents = fixer.get_fixed_contents(file_path)

    print(fixed_contents)
