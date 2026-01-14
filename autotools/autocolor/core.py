import re
import colorsys
import pyperclip

# CONVERTS HEX COLOR TO RGB TUPLE
def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif len(hex_color) == 8:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        alpha = int(hex_color[6:8], 16) / 255.0
        return (*rgb, alpha)
    raise ValueError(f"INVALID HEX COLOR: {hex_color}")

# CONVERTS RGB TUPLE TO HEX
def _rgb_to_hex(r, g, b, alpha=None):
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    if alpha is not None: hex_color += f"{int(alpha * 255):02x}"
    return hex_color.upper()

# PARSES RGB/RGBA STRING
def _parse_rgb(rgb_str):
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', rgb_str.lower())
    if not match: raise ValueError(f"INVALID RGB/RGBA FORMAT: {rgb_str}")
    r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
    alpha = float(match.group(4)) if match.group(4) else None
    if alpha is not None and alpha > 1:
        alpha = alpha / 255.0
    return (r, g, b, alpha) if alpha is not None else (r, g, b)

# PARSES HSL/HSLA STRING
def _parse_hsl(hsl_str):
    match = re.match(r'hsla?\((\d+),\s*(\d+)%,\s*(\d+)%(?:,\s*([\d.]+))?\)', hsl_str.lower())
    if not match: raise ValueError(f"INVALID HSL/HSLA FORMAT: {hsl_str}")
    h = int(match.group(1)) / 360.0
    s = int(match.group(2)) / 100.0
    l = int(match.group(3)) / 100.0
    alpha = float(match.group(4)) if match.group(4) else None
    return (h, s, l, alpha) if alpha is not None else (h, s, l)

# PARSES INPUT COLOR AND RETURNS RGB VALUES WITH ALPHA
def _parse_color_input(color_input):
    if color_input.startswith('#'):
        rgb_result = _hex_to_rgb(color_input)
        return rgb_result if len(rgb_result) == 4 else (*rgb_result, None)
    elif color_input.startswith('rgb'):
        rgb_result = _parse_rgb(color_input)
        return rgb_result if len(rgb_result) == 4 else (*rgb_result, None)
    elif color_input.startswith('hsl'):
        hsl_result = _parse_hsl(color_input)
        if len(hsl_result) == 4:
            h, s, l, alpha = hsl_result
        else:
            h, s, l = hsl_result
            alpha = None
        r, g, b = [int(c * 255) for c in colorsys.hls_to_rgb(h, l, s)]
        return (r, g, b, alpha)
    raise ValueError(f"UNSUPPORTED COLOR FORMAT: {color_input}")

# CONVERTS RGB TO HSL VALUES
def _rgb_to_hsl_values(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return (int(h * 360), int(s * 100), int(l * 100))

# FORMATS OUTPUT COLOR BASED ON FORMAT TYPE
def _format_output(r, g, b, alpha, output_format):
    if output_format == 'hex':
        return _rgb_to_hex(r, g, b, alpha)
    elif output_format == 'rgb':
        return f"rgb({r}, {g}, {b})"
    elif output_format == 'rgba':
        alpha = alpha if alpha is not None else 1.0
        return f"rgba({r}, {g}, {b}, {alpha:.2f})"
    elif output_format == 'hsl':
        h, s, l = _rgb_to_hsl_values(r, g, b)
        return f"hsl({h}, {s}%, {l}%)"
    elif output_format == 'hsla':
        alpha = alpha if alpha is not None else 1.0
        h, s, l = _rgb_to_hsl_values(r, g, b)
        return f"hsla({h}, {s}%, {l}%, {alpha:.2f})"
    raise ValueError(f"UNSUPPORTED OUTPUT FORMAT: {output_format}")

# CONVERTS COLOR CODE TO DIFFERENT FORMATS
def autocolor_convert(color_input, output_format='hex'):
    color_input = color_input.strip()
    output_format = output_format.lower()
    
    r, g, b, alpha = _parse_color_input(color_input)
    result = _format_output(r, g, b, alpha, output_format)

    try: pyperclip.copy(result)
    except pyperclip.PyperclipException: pass
    
    return result
