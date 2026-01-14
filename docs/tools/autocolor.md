# AutoColor

## Description

Converts color codes between different formats (HEX, RGB, RGBA, HSL, HSLA) and automatically copies the result to your clipboard.

## Supported Input Formats

-   **HEX**: `#RRGGBB`, `#RRGGBBAA`, `#RGB` (3-character shorthand)
-   **RGB**: `rgb(r, g, b)` where r, g, b are integers 0-255
-   **RGBA**: `rgba(r, g, b, a)` where r, g, b are integers 0-255 and a is 0.0-1.0 or 0-255
-   **HSL**: `hsl(h, s%, l%)` where h is 0-360, s and l are 0-100%
-   **HSLA**: `hsla(h, s%, l%, a)` where h is 0-360, s and l are 0-100%, a is 0.0-1.0

## Supported Output Formats

-   `hex` - Hexadecimal format (default)
-   `rgb` - RGB format
-   `rgba` - RGBA format with alpha channel
-   `hsl` - HSL format
-   `hsla` - HSLA format with alpha channel

## Usage

```bash
autocolor <color_code> [--format <output_format>]
```

### Options

-   `--format, -f`: Output format (hex, rgb, rgba, hsl, hsla). Default: hex

## Examples

### Basic Conversions

```bash
# Convert HEX to default format (HEX)
autocolor "#FF5733"
# Output: #FF5733

# Convert RGB to HEX
autocolor "rgb(255, 87, 51)" --format hex
# Output: #FF5733

# Convert HEX to RGB
autocolor "#FF5733" --format rgb
# Output: rgb(255, 87, 51)

# Convert HEX to HSL
autocolor "#FF5733" --format hsl
# Output: hsl(9, 100%, 60%)

# Convert HSL to HEX
autocolor "hsl(9, 100%, 60%)" --format hex
# Output: #FF5733
```

### Format Conversions

```bash
# HEX to RGBA
autocolor "#FF5733" --format rgba
# Output: rgba(255, 87, 51, 1.00)

# RGB to HSLA
autocolor "rgb(255, 87, 51)" --format hsla
# Output: hsla(9, 100%, 60%, 1.00)

# RGBA to HEX
autocolor "rgba(255, 87, 51, 0.5)" --format hex
# Output: #FF573380

# HSLA to RGB
autocolor "hsla(9, 100%, 60%, 0.5)" --format rgb
# Output: rgb(255, 87, 51)
```

### Short HEX Format

```bash
# 3-character HEX shorthand
autocolor "#F73"
# Output: #FF7733

# 8-character HEX with alpha
autocolor "#FF5733FF"
# Output: #FF5733FF
```

### Case Insensitive

```bash
# Format option is case insensitive
autocolor "#FF5733" --format RGB
autocolor "#FF5733" --format HsL
autocolor "#FF5733" --format RGBA
```

## Notes

-   The converted color is automatically copied to your clipboard
-   Input formats are case insensitive (RGB, rgb, Rgb all work)
-   Spaces in color codes are automatically trimmed
-   Alpha values greater than 1 in RGBA are normalized to 0.0-1.0 range
-   When converting to RGBA/HSLA without an alpha value, alpha defaults to 1.0
-   HEX output is always uppercase
-   RGB/RGBA values are rounded to integers
-   HSL/HSLA percentages are rounded to integers, alpha is rounded to 2 decimal places
