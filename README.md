# conv

`conv` is a tiny Python CLI that leans on Pillow to inspect or convert raster images between the commonly supported formats.

## Requirements

- Python 3.8+ (any recent 3.x)
- [Pillow](https://python-pillow.org/)

Install Pillow once so `conv` can import it:

```bash
pip install pillow
```

## Usage

```bash
# conversion with positional arguments
conv input.webp png

# the same conversion using flags
conv -i input.webp -f png

# metadata/info display (any single path is treated as `--info`)
conv image.png

# explicit info flag
conv --info image.png
```

### Flags & Commands

| Command | Description |
|--------|-------------|
| `conv INPUT FORMAT` <br> `conv -i INPUT -f FORMAT` | Convert the file to the requested format (png, webp, jpeg, avif). Output is written next to the input file with the new extension. |
| `conv --info FILE` or `conv FILE` | Show metadata and basic diagnostics for the image.
| `conv --formats` | Print the list of formats supported by this build of Pillow.
| `conv --version` | Show the CLI version.
| `conv --doctor` | Check the environment for Pillow and optional features such as AVIF support. |

Notes:

- JPEG targets strip alpha channels automatically (images are converted to RGB).
- AVIF conversions only work when Pillow is compiled with AVIF codecs; run `conv --doctor` to verify.
- Errors clearly report issues such as missing files, unsupported formats, or unreadable images.

## Examples

```bash
conv photo.avif jpeg        # convert AVIF to JPEG
conv sprite.png webp        # convert PNG to WebP
conv --info banner.webp     # show metadata
conv --formats              # list supported formats
conv --doctor               # verify environment
```

## Why it exists?

This is a small tool built while experimenting with Codex
