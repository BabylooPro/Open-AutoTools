import pytest
import pyperclip
from autotools.autocolor.core import (autocolor_convert, _hex_to_rgb, _rgb_to_hex, _parse_rgb, _parse_hsl)

# HELPER FUNCTIONS

# HELPER TO CHECK FLOATING POINT VALUES WITH TOLERANCE
def assert_float_equal(actual, expected, tolerance=0.01):
    assert abs(actual - expected) < tolerance

# HELPER TO CHECK HSL/HSLA FORMAT
def assert_hsl_format(result):
    assert "hsl(" in result or "hsla(" in result
    assert "%" in result

# UNIT TESTS

# TESTS FOR _hex_to_rgb

# TEST FOR 6-CHARACTER HEX
def test_hex_to_rgb_6_char():
    assert _hex_to_rgb("#FF5733") == (255, 87, 51)
    assert _hex_to_rgb("#000000") == (0, 0, 0)
    assert _hex_to_rgb("#FFFFFF") == (255, 255, 255)
    assert _hex_to_rgb("FF5733") == (255, 87, 51)

# TEST FOR 3-CHARACTER HEX
def test_hex_to_rgb_3_char():
    assert _hex_to_rgb("#F73") == (255, 119, 51)
    assert _hex_to_rgb("#000") == (0, 0, 0)
    assert _hex_to_rgb("#FFF") == (255, 255, 255)

# TEST FOR 8-CHARACTER HEX WITH ALPHA
@pytest.mark.parametrize("hex_color,expected_rgb,expected_alpha", [
    ("#FF5733FF", (255, 87, 51), 1.0),
    ("#FF573300", (255, 87, 51), 0.0),
    ("#FF573380", (255, 87, 51), 0.5),
])
def test_hex_to_rgb_8_char(hex_color, expected_rgb, expected_alpha):
    result = _hex_to_rgb(hex_color)
    assert result[:3] == expected_rgb
    assert_float_equal(result[3], expected_alpha)

# TEST FOR INVALID HEX
def test_hex_to_rgb_invalid():
    with pytest.raises(ValueError): _hex_to_rgb("#GGGGGG")
    with pytest.raises(ValueError, match="INVALID HEX COLOR"): _hex_to_rgb("#FF")
    with pytest.raises(ValueError, match="INVALID HEX COLOR"): _hex_to_rgb("#FFFFF")

# TESTS FOR _rgb_to_hex

# TEST FOR RGB TO HEX WITHOUT ALPHA
def test_rgb_to_hex_no_alpha():
    assert _rgb_to_hex(255, 87, 51) == "#FF5733"
    assert _rgb_to_hex(0, 0, 0) == "#000000"
    assert _rgb_to_hex(255, 255, 255) == "#FFFFFF"
    assert _rgb_to_hex(10, 20, 30) == "#0A141E"

# TEST FOR RGB TO HEX WITH ALPHA
def test_rgb_to_hex_with_alpha():
    assert _rgb_to_hex(255, 87, 51, 1.0) == "#FF5733FF"
    assert _rgb_to_hex(255, 87, 51, 0.0) == "#FF573300"
    assert _rgb_to_hex(255, 87, 51, 0.5) == "#FF57337F"

# TESTS FOR _parse_rgb

# TEST FOR RGB PARSING
@pytest.mark.parametrize("rgb_str,expected", [
    ("rgb(255, 87, 51)", (255, 87, 51)),
    ("rgb(0, 0, 0)", (0, 0, 0)),
    ("rgb(255, 255, 255)", (255, 255, 255)),
    ("RGB(255, 87, 51)", (255, 87, 51)),
])
def test_parse_rgb_basic(rgb_str, expected):
    assert _parse_rgb(rgb_str) == expected

# TEST FOR RGB PARSING WITH SPACES
def test_parse_rgb_with_spaces():
    assert _parse_rgb("rgb(255,  87,  51)") == (255, 87, 51)
    assert _parse_rgb("rgb(255, 87, 51)") == (255, 87, 51)

# TEST FOR RGBA PARSING
@pytest.mark.parametrize("rgba_str,expected_rgb,expected_alpha", [
    ("rgba(255, 87, 51, 1.0)", (255, 87, 51), 1.0),
    ("rgba(255, 87, 51, 0.5)", (255, 87, 51), 0.5),
])
def test_parse_rgba_basic(rgba_str, expected_rgb, expected_alpha):
    result = _parse_rgb(rgba_str)
    assert result[:3] == expected_rgb
    assert_float_equal(result[3], expected_alpha)

# TEST FOR RGBA WITH ALPHA > 1 (SHOULD NORMALIZE)
def test_parse_rgba_alpha_gt_1():
    result = _parse_rgb("rgba(255, 87, 51, 255)")
    assert result[:3] == (255, 87, 51)
    assert abs(result[3] - 1.0) < 0.01

# TEST FOR INVALID RGB FORMAT
@pytest.mark.parametrize("invalid_rgb", [
    "rgb(255, 87)",
    "rgb(255, 87, 51, 1.0, 2.0)",
    "invalid",
])
def test_parse_rgb_invalid(invalid_rgb):
    with pytest.raises(ValueError, match="INVALID RGB/RGBA FORMAT"): _parse_rgb(invalid_rgb)

# TESTS FOR _parse_hsl

# TEST FOR HSL PARSING
@pytest.mark.parametrize("hsl_str,expected_h,expected_s,expected_l", [
    ("hsl(9, 100%, 60%)", 9/360.0, 1.0, 0.6),
    ("HSL(0, 0%, 0%)", 0.0, 0.0, 0.0),
    ("HSL(360, 100%, 100%)", 1.0, 1.0, 1.0),
])
def test_parse_hsl_basic(hsl_str, expected_h, expected_s, expected_l):
    result = _parse_hsl(hsl_str)
    assert_float_equal(result[0], expected_h)
    assert_float_equal(result[1], expected_s)
    assert_float_equal(result[2], expected_l)

# TEST FOR HSL PARSING WITH SPACES
def test_parse_hsl_with_spaces():
    result = _parse_hsl("hsl(9,  100%,  60%)")
    assert abs(result[1] - 1.0) < 0.01
    assert abs(result[2] - 0.6) < 0.01

# TEST FOR HSLA PARSING
@pytest.mark.parametrize("hsla_str,expected_alpha", [
    ("hsla(9, 100%, 60%, 1.0)", 1.0),
    ("hsla(9, 100%, 60%, 0.5)", 0.5),
])
def test_parse_hsla_basic(hsla_str, expected_alpha):
    result = _parse_hsl(hsla_str)
    assert len(result) == 4
    assert_float_equal(result[3], expected_alpha)

# TEST FOR INVALID HSL FORMAT
@pytest.mark.parametrize("invalid_hsl", [
    "hsl(9, 100%)",
    "hsl(9, 100%, 60%, 1.0, 2.0)",
    "invalid",
])
def test_parse_hsl_invalid(invalid_hsl):
    with pytest.raises(ValueError, match="INVALID HSL/HSLA FORMAT"): _parse_hsl(invalid_hsl)

# TESTS FOR autocolor_convert - HEX INPUT

# TEST FOR HEX TO HEX
def test_autocolor_convert_hex_to_hex():
    assert autocolor_convert("#FF5733", "hex") == "#FF5733"
    assert autocolor_convert("#F73", "hex") == "#FF7733"
    assert autocolor_convert("#000000", "hex") == "#000000"

# TEST FOR HEX TO RGB
def test_autocolor_convert_hex_to_rgb():
    result = autocolor_convert("#FF5733", "rgb")
    assert result == "rgb(255, 87, 51)"
    assert autocolor_convert("#000000", "rgb") == "rgb(0, 0, 0)"

# TEST FOR HEX TO RGBA
def test_autocolor_convert_hex_to_rgba():
    result = autocolor_convert("#FF5733", "rgba")
    assert "rgba(255, 87, 51" in result
    assert autocolor_convert("#FF5733FF", "rgba") == "rgba(255, 87, 51, 1.00)"

# TEST FOR HEX TO HSL/HSLA
@pytest.mark.parametrize("output_format,has_alpha", [
    ("hsl", False),
    ("hsla", True),
])
def test_autocolor_convert_hex_to_hsl_formats(output_format, has_alpha):
    result = autocolor_convert("#FF5733", output_format)
    assert_hsl_format(result)
    if has_alpha: assert "1.00" in result

# TESTS FOR autocolor_convert - RGB INPUT

# TEST FOR RGB TO HEX
def test_autocolor_convert_rgb_to_hex():
    assert autocolor_convert("rgb(255, 87, 51)", "hex") == "#FF5733"
    assert autocolor_convert("rgb(0, 0, 0)", "hex") == "#000000"

# TEST FOR RGB TO RGB
def test_autocolor_convert_rgb_to_rgb():
    result = autocolor_convert("rgb(255, 87, 51)", "rgb")
    assert result == "rgb(255, 87, 51)"

# TEST FOR RGB TO RGBA
def test_autocolor_convert_rgb_to_rgba():
    result = autocolor_convert("rgb(255, 87, 51)", "rgba")
    assert result == "rgba(255, 87, 51, 1.00)"

# TEST FOR RGB TO HSL
def test_autocolor_convert_rgb_to_hsl():
    result = autocolor_convert("rgb(255, 87, 51)", "hsl")
    assert_hsl_format(result)

# TEST FOR RGB/RGBA TO HSLA (COVERS BOTH BRANCHES)
@pytest.mark.parametrize("input_color,expected_alpha", [
    ("rgb(255, 87, 51)", "1.00"),  # ALPHA IS NONE
    ("rgba(255, 87, 51, 0.5)", "0.50"),  # ALPHA IS NOT NONE
])
def test_autocolor_convert_to_hsla(input_color, expected_alpha):
    result = autocolor_convert(input_color, "hsla")
    assert_hsl_format(result)
    assert expected_alpha in result

# TESTS FOR autocolor_convert - RGBA INPUT

# TEST FOR RGBA TO HEX
def test_autocolor_convert_rgba_to_hex():
    result = autocolor_convert("rgba(255, 87, 51, 1.0)", "hex")
    assert result == "#FF5733FF"
    result = autocolor_convert("rgba(255, 87, 51, 0.5)", "hex")
    assert "#FF5733" in result

# TEST FOR RGBA TO RGB
def test_autocolor_convert_rgba_to_rgb():
    result = autocolor_convert("rgba(255, 87, 51, 1.0)", "rgb")
    assert result == "rgb(255, 87, 51)"

# TEST FOR RGBA TO RGBA
def test_autocolor_convert_rgba_to_rgba():
    result = autocolor_convert("rgba(255, 87, 51, 0.5)", "rgba")
    assert "rgba(255, 87, 51, 0.50)" in result

# TESTS FOR autocolor_convert - HSL INPUT

# TEST FOR HSL TO DIFFERENT FORMATS
@pytest.mark.parametrize("output_format,expected_start", [
    ("hex", "#"),
    ("rgb", "rgb("),
    ("hsl", "hsl("),
])
def test_autocolor_convert_hsl_to_formats(output_format, expected_start):
    result = autocolor_convert("hsl(9, 100%, 60%)", output_format)
    assert result.startswith(expected_start)
    if output_format == "hex": assert len(result) == 7
    elif output_format == "hsl": assert_hsl_format(result)

# TESTS FOR autocolor_convert - HSLA INPUT

# TEST FOR HSLA TO HEX/RGBA
@pytest.mark.parametrize("output_format,check_func", [
    ("hex", lambda r: r.startswith("#")),
    ("rgba", lambda r: "rgba(" in r),
])
def test_autocolor_convert_hsla_to_formats(output_format, check_func):
    result = autocolor_convert("hsla(9, 100%, 60%, 0.5)", output_format)
    assert check_func(result)

# TEST FOR HSL TO HSLA (WITHOUT ALPHA - COVERS BRANCH)
def test_autocolor_convert_hsl_to_hsla():
    result = autocolor_convert("hsl(9, 100%, 60%)", "hsla")
    assert_hsl_format(result)
    assert "1.00" in result

# TESTS FOR ERROR HANDLING

# TEST FOR UNSUPPORTED INPUT FORMAT
def test_autocolor_convert_unsupported_input():
    with pytest.raises(ValueError, match="UNSUPPORTED COLOR FORMAT"): autocolor_convert("invalid", "hex")

# TEST FOR UNSUPPORTED OUTPUT FORMAT
def test_autocolor_convert_unsupported_output():
    with pytest.raises(ValueError, match="UNSUPPORTED OUTPUT FORMAT"): autocolor_convert("#FF5733", "invalid")

# TEST FOR WHITESPACE HANDLING
def test_autocolor_convert_whitespace():
    assert autocolor_convert("  #FF5733  ", "hex") == "#FF5733"
    assert autocolor_convert("  rgb(255, 87, 51)  ", "hex") == "#FF5733"

# TEST FOR CASE INSENSITIVE OUTPUT FORMAT
@pytest.mark.parametrize("output_format,expected", [
    ("HEX", "#FF5733"),
    ("RGB", "rgb(255, 87, 51)"),
    ("RgBa", "rgba(255, 87, 51, 1.00)"),
])
def test_autocolor_convert_case_insensitive(output_format, expected):
    assert autocolor_convert("#FF5733", output_format) == expected

# TEST FOR PYPERCLIP EXCEPTION HANDLING
def test_autocolor_convert_pyperclip_exception(monkeypatch):
    def mock_copy_fail(text): raise pyperclip.PyperclipException("Clipboard error")
    monkeypatch.setattr(pyperclip, "copy", mock_copy_fail)
    result = autocolor_convert("#FF5733", "hex")
    assert result == "#FF5733"

# TEST FOR ROUND-TRIP CONVERSIONS
def test_autocolor_convert_round_trip():
    hex_color = "#FF5733"
    rgb_result = autocolor_convert(hex_color, "rgb")
    hex_result = autocolor_convert(rgb_result, "hex")
    assert hex_result == hex_color
    
    rgb_color = "rgb(255, 87, 51)"
    hsl_result = autocolor_convert(rgb_color, "hsl")
    rgb_result2 = autocolor_convert(hsl_result, "rgb")
    assert "rgb(255" in rgb_result2 or "rgb(254" in rgb_result2
