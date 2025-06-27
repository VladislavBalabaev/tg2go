import argparse
import os
from pathlib import Path

DIR_ROOT = Path(__file__).resolve().parent.parent
DIR_SRC = DIR_ROOT / "src"

output_file = "code_combined.txt"

parser = argparse.ArgumentParser(description="Combine .py files into one.")
parser.add_argument(
    "--src",
    type=Path,
    default=DIR_SRC,
    help="Source directory to search for Python files.",
)
args = parser.parse_args()


with open(output_file, "w", encoding="utf-8") as outfile:
    for dirpath, _, filenames in os.walk(args.src.resolve()):
        for filename in sorted(filenames):
            if filename.endswith(".py") and filename != "__init__.py":
                filepath = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(filepath, DIR_SRC)

                outfile.write(f"# === {relative_path} ===\n")

                with open(filepath, encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n")


print(f"Combined file saved as: {output_file}")  # noqa: T201
