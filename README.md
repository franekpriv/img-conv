# conv

A small Python CLI for converting images between formats using Pillow.

## Usage

```bash
# convert (positional)
conv input.webp png

# convert (flags)
conv -i input.webp -f png

# quick info (single arg)
conv image.png

# explicit info flag
conv --info image.png

# supported formats
conv --formats

# environment check
conv --doctor

# version
conv --version
```

## Install dependencies

```bash
pip install pillow
```

## Notes

- Supports png, webp, jpeg, avif (jpg aliases to jpeg).
- Output is saved alongside the input file with the new extension.
- AVIF requires Pillow built with AVIF support.
