# conv

Small Python CLI for converting images with Pillow.

## Install

```bash
pip install pillow
```

## Quick Start

```bash
# convert (positional)
conv input.webp png

# convert (flags)
conv -i input.webp -f png

# quick info (single arg)
conv image.png

# explicit info flag
conv --info image.png
```

## Commands

- Convert: `conv INPUT FORMAT` or `conv -i INPUT -f FORMAT`
- Info: `conv --info FILE` or `conv FILE` (single arg)
- Formats: `conv --formats`
- Version: `conv --version`
- Doctor: `conv --doctor`

## Behavior

- Supported formats: png, webp, jpeg, avif (jpg aliases to jpeg).
- Output is written next to the input with the new extension.
- JPEG targets auto-convert alpha images to RGB.
- AVIF works if your Pillow build has AVIF support (`conv --doctor` to check).
- Errors are clear for missing files, bad formats, or unreadable images.

## Examples

```bash
conv photo.avif jpeg        # convert AVIF to JPEG
conv sprite.png webp        # convert PNG to WebP
conv --info banner.webp     # show metadata
conv --formats              # list supported formats
conv --doctor               # verify environment
```

## Also it's vibecoded!
It's just a simple tool for me, just wanted to test out OpenAI's codex.
