import argparse

from builder import IndexBuilder


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")

    args = parser.parse_args()
    file_path = args.file_path

    builder = IndexBuilder()
    index_path = builder.build_index(file_path)
