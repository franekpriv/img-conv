# conv Error/Success Codes

Use these codes to quickly identify what happened when running `conv`.

## Success Codes

| Code | When it appears | Description | Simple fix/action |
|---|---|---|---|
| `01` | `conv --formats` | Supported output formats were listed. | No fix needed. Pick one listed format for conversion. |
| `02` | `conv --version` | Tool version was printed. | No fix needed. Use this to confirm installed version. |
| `03` | `conv --doctor` | Environment diagnostics were printed. | If AVIF is `no`, install a Pillow build with AVIF support. |
| `04` | `conv FILE` or `conv --info FILE` | Image metadata was read successfully. | No fix needed. |
| `05` | `conv INPUT FORMAT` | Conversion completed and output file was saved. | No fix needed. Verify output file path in message. |

## Error Codes

| Code | When it appears | Description | Simple fix |
|---|---|---|---|
| `06` | Missing input file path | Input file does not exist at the given path. | Check file path and filename, then retry. |
| `07` | Invalid/non-image file | Pillow cannot identify the file as an image. | Use a valid image file (png/webp/jpeg/avif source). |
| `08` | Read failure during info | File exists but metadata read failed (permissions/corruption). | Check file permissions and integrity, then retry. |
| `09` | Reserved keyword used as file | `formats/info/version/doctor` was used as positional file input. | Use the explicit flag (for example `--formats`) or a real file path. |
| `10` | Missing required args | Conversion mode was used without both input and target format. | Run `conv INPUT FORMAT` or `conv -i INPUT -f FORMAT`. |
| `11` | Unsupported output format | Requested target format is not supported. | Use one of: `png`, `webp`, `jpeg`, `avif`. |
| `12` | Convert write/process failure | Conversion failed while saving/processing image. | Check destination permissions, disk space, and source file validity. |
| `13` | Invalid CLI arguments | CLI arguments are malformed (for example missing value for `--info`). | Run `conv -h` and retry with valid argument syntax. |
