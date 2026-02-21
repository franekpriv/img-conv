#!/usr/bin/env bash
set -euo pipefail

# Install conv as a user-level command at ~/.local/bin/conv.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SCRIPT="$SCRIPT_DIR/conv.py"
TARGET_DIR="${HOME}/.local/bin"
TARGET_BIN="$TARGET_DIR/conv"

echo "start"
echo "script_dir=$SCRIPT_DIR"
echo "source_script=$SOURCE_SCRIPT"
echo "target_bin=$TARGET_BIN"

if [[ "${OSTYPE:-}" != linux* ]]; then
  echo "this installer supports Linux only" >&2
  exit 1
fi

echo "linux check passed"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found" >&2
  exit 1
fi

echo "python3 found at $(command -v python3)"

if [[ ! -f "$SOURCE_SCRIPT" ]]; then
  echo "could not find conv.py at $SOURCE_SCRIPT" >&2
  exit 1
fi

echo "source file exists"

if ! python3 -c "import PIL" >/dev/null 2>&1; then
  echo "pillow not found"
  if ! command -v pip3 >/dev/null 2>&1; then
    echo "error: pip3 is required to install Pillow automatically" >&2
    echo "install pip3 and run: pip3 install --user pillow" >&2
    exit 1
  fi
  read -r -p "Install Pillow now with pip3 --user? [y/N]: " install_pillow
  if [[ ! "$install_pillow" =~ ^[Yy]$ ]]; then
    echo "installation cancelled: Pillow is required for conv"
    echo "install manually with: pip3 install --user pillow"
    exit 1
  fi
  echo "pip3 found at $(command -v pip3)"
  pip3 install --user pillow
  echo "pillow install done"
else
  echo "pillow already installed"
fi

echo "ensuring target directory exists"
mkdir -p "$TARGET_DIR"
echo "copying script into target location"
cp "$SOURCE_SCRIPT" "$TARGET_BIN"
echo "making target executable"
chmod +x "$TARGET_BIN"

echo "installed in $TARGET_BIN"

case ":$PATH:" in
  *":$TARGET_DIR:"*)
    echo "PATH already includes $TARGET_DIR"
    echo "running: conv --version"
    conv --version
    ;;
  *)
    echo "warning: $TARGET_DIR is not on PATH in this shell"
    echo "add this to your shell config:"
    echo "  export PATH=\"$HOME/.local/bin:\$PATH\""
    ;;
esac

echo "done"
