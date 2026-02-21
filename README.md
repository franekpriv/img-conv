# conv

`conv` is a small Python CLI for image conversion and image info output.

## Requirements

- Python 3.8+
- [Pillow](https://python-pillow.org/)

## Install (Linux)

From the project root:

```bash
chmod +x install_linux.sh
./install_linux.sh
```

Installer behavior:

- Checks Linux + `python3`.
- If Pillow is missing, asks before running `pip3 install --user pillow`.
- Installs the command to `~/.local/bin/conv`.
- Warns if `~/.local/bin` is not on `PATH`.

Verify:

```bash
conv --version
```

If `~/.local/bin` is not on `PATH`, add:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

```bash
# Convert
conv input.webp png
conv -i input.webp -f png

# Info
conv image.png
conv --info image.png
```

## Commands

| Command | Description |
|---|---|
| `conv INPUT FORMAT` | Convert image format. |
| `conv -i INPUT -f FORMAT` | Convert image format (flag form). |
| `conv FILE` | Show image info. |
| `conv --info FILE` | Show image info (explicit flag). |
| `conv --formats` | List supported output formats. |
| `conv --doctor` | Print environment diagnostics. |
| `conv --version` | Print CLI version. |
| `conv -h` | Show custom help text. |

## Notes

- Supported formats: `png`, `webp`, `jpeg`, `avif` (`jpg` aliases to `jpeg`).
- JPEG output auto-converts alpha images to RGB.
- AVIF depends on your Pillow build (`conv --doctor`).
- Output file is written beside the input with the new extension.
- Success and error outputs include numeric codes; see `error_codes.md`.

## Examples

```bash
conv photo.avif jpeg
conv sprite.png webp
conv --info banner.webp
conv --formats
conv --doctor
```
