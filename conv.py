#!/usr/bin/env python3
"""conv: Simple image format converter.

Dependencies:
  pip install pillow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, UnidentifiedImageError, __version__ as pillow_version
from PIL import features as pillow_features


VERSION = "0.3"
SUPPORTED_FORMATS = {"png", "webp", "jpeg", "avif"}
HELP_TEXT = """Conv-rt help:

Converting a file to another format:
  conv [FILE] [FORMAT]
  conv -i [FILE] -f [FORMAT]

Showing information about a file:
  conv [FILE]
  conv -i [FILE]
  conv --info [FILE]

Misc:
  conv --doctor
  conv --formats
  conv --version
"""
SUCCESS_CODES = {
    "formats_listed": "01",
    "version_shown": "02",
    "doctor_shown": "03",
    "image_info_shown": "04",
    "image_converted": "05",
}
ERROR_CODES = {
    "input_missing": "06",
    "not_image": "07",
    "read_failed": "08",
    "reserved_keyword": "09",
    "missing_args": "10",
    "unsupported_format": "11",
    "convert_failed": "12",
    "bad_arguments": "13",
}
# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def print_success(code: str, message: str) -> None:
    print(f"[{code}] {message}")


def print_error(code: str, message: str) -> None:
    print(f"[{code}] Error: {message}", file=sys.stderr)


class ConvArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        print_error(ERROR_CODES["bad_arguments"], message)
        raise SystemExit(2)


def normalize_format(fmt: str) -> str:
    """Normalize format strings (e.g., jpg -> jpeg)."""
    fmt = fmt.lower().lstrip(".")
    if fmt == "jpg":
        return "jpeg"
    return fmt


def build_output_path(input_path: Path, target_format: str) -> Path:
    """Build output path in the same directory as input."""
    return input_path.with_suffix(f".{target_format}")


def convert_image(input_path: Path, target_format: str) -> Path:
    """Convert the image and return output path.

    Raises:
        FileNotFoundError: if input file does not exist
        ValueError: if target format is unsupported
        UnidentifiedImageError: if Pillow cannot identify the image
        OSError: for other image I/O errors
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    target_format = normalize_format(target_format)
    if target_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported target format '{target_format}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}."
        )

    output_path = build_output_path(input_path, target_format)

    with Image.open(input_path) as img:
        # Ensure conversion for formats that don't support alpha
        if target_format == "jpeg" and img.mode in {"RGBA", "LA", "P"}:
            img = img.convert("RGB")
        img.save(output_path, format=target_format.upper())

    return output_path


def get_image_info(input_path: Path) -> dict:
    """Return basic image info."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    with Image.open(input_path) as img:
        size_bytes = input_path.stat().st_size
        return {
            "format": (img.format or "unknown").lower(),
            "width": img.width,
            "height": img.height,
            "mode": img.mode,
            "size_bytes": size_bytes,
        }


def supports_avif() -> bool:
    """Check whether Pillow supports AVIF in this environment."""
    try:
        return bool(pillow_features.check("avif"))
    except Exception:
        return any(ext.lower() == ".avif" for ext in Image.registered_extensions().keys())


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = ConvArgumentParser(
        add_help=False,
        prog="conv",
    )
    parser.add_argument("-h", "--help", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--formats", action="store_true", help="Print supported formats")
    parser.add_argument("--info", metavar="FILE", help="Print image information")
    parser.add_argument("--version", action="store_true", help="Print tool version")
    parser.add_argument("--doctor", action="store_true", help="Check environment and AVIF support")

    parser.add_argument("input_file", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("target_format", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument(
        "-i",
        "--input",
        dest="input_file_opt",
        help="Path to the input image file",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="target_format_opt",
        help="Target format: png, webp, jpeg, avif",
    )

    return parser.parse_args(list(argv))


def show_image_info(input_path: Path) -> int:
    try:
        info = get_image_info(input_path)
    except FileNotFoundError as exc:
        print_error(ERROR_CODES["input_missing"], str(exc))
        return 1
    except UnidentifiedImageError:
        print_error(ERROR_CODES["not_image"], "Pillow could not identify the input file as an image.")
        return 1
    except OSError as exc:
        print_error(ERROR_CODES["read_failed"], f"Failed to read image: {exc}")
        return 1

    print_success(SUCCESS_CODES["image_info_shown"], "Image information:")
    print(f"Format: {info['format']}")
    print(f"Dimensions: {info['width']}x{info['height']}")
    print(f"Mode: {info['mode']}")
    print(f"File size: {info['size_bytes']} bytes")
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.help:
        print(HELP_TEXT, end="")
        return 0
    if args.formats:
        print_success(
            SUCCESS_CODES["formats_listed"],
            "Supported formats: " + ", ".join(sorted(SUPPORTED_FORMATS)),
        )
        return 0
    if args.version:
        print_success(SUCCESS_CODES["version_shown"], f"Version: {VERSION}")
        return 0
    if args.doctor:
        py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        avif = "yes" if supports_avif() else "no"
        print_success(SUCCESS_CODES["doctor_shown"], "Environment diagnostics:")
        print(f"Python: {py}")
        print(f"Pillow: {pillow_version}")
        print(f"AVIF support: {avif}")
        return 0
    if args.info:
        return show_image_info(Path(args.info))

    input_file = args.input_file or args.input_file_opt
    target_format = args.target_format or args.target_format_opt

    reserved = {"formats", "info", "version", "doctor"}
    if input_file in reserved and not target_format:
        print_error(
            ERROR_CODES["reserved_keyword"],
            f"'{input_file}' is a reserved keyword. Use --{input_file} instead.",
        )
        return 1

    if not input_file or not target_format:
        if input_file and not target_format:
            return show_image_info(Path(input_file))
        print_error(ERROR_CODES["missing_args"], "input file and target format are required.")
        return 1

    input_path = Path(input_file)

    try:
        output_path = convert_image(input_path, target_format)
    except FileNotFoundError as exc:
        print_error(ERROR_CODES["input_missing"], str(exc))
        return 1
    except ValueError as exc:
        print_error(ERROR_CODES["unsupported_format"], str(exc))
        return 1
    except UnidentifiedImageError:
        print_error(ERROR_CODES["not_image"], "Pillow could not identify the input file as an image.")
        return 1
    except OSError as exc:
        print_error(ERROR_CODES["convert_failed"], f"Failed to convert image: {exc}")
        return 1

    print_success(SUCCESS_CODES["image_converted"], f"Saved converted file to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
