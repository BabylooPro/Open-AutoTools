import pytest
import pyperclip
from autotools.autounit.core import autounit_convert

# HELPER TO CHECK FLOATING POINT VALUES WITH TOLERANCE
def assert_float_equal(actual, expected, tolerance=0.01):
    assert abs(actual - expected) < tolerance

# HELPER TO EXTRACT VALUE FROM OUTPUT
def extract_value(output_str):
    return float(output_str.split()[0])

# TESTS FOR LENGTH CONVERSIONS

# TEST FOR METERS TO FEET
def test_autounit_convert_meters_to_feet():
    result = autounit_convert("100", "meter", "feet")
    value = extract_value(result)
    assert_float_equal(value, 328.084, tolerance=0.1)
    assert "feet" in result

# TEST FOR FEET TO METERS
def test_autounit_convert_feet_to_meters():
    result = autounit_convert("328.084", "feet", "meter")
    value = extract_value(result)
    assert_float_equal(value, 100, tolerance=0.1)
    assert "meter" in result

# TEST FOR KILOMETERS TO MILES
def test_autounit_convert_kilometers_to_miles():
    result = autounit_convert("1", "kilometer", "mile")
    value = extract_value(result)
    assert_float_equal(value, 0.621371, tolerance=0.01)
    assert "mile" in result

# TEST FOR INCHES TO CENTIMETERS
def test_autounit_convert_inches_to_centimeters():
    result = autounit_convert("1", "inch", "centimeter")
    value = extract_value(result)
    assert_float_equal(value, 2.54, tolerance=0.01)
    assert "centimeter" in result

# TESTS FOR VOLUME CONVERSIONS

# TEST FOR LITERS TO GALLONS
def test_autounit_convert_liters_to_gallons():
    result = autounit_convert("10", "liter", "gallon")
    value = extract_value(result)
    assert_float_equal(value, 2.64172, tolerance=0.01)
    assert "gallon" in result

# TEST FOR GALLONS TO LITERS
def test_autounit_convert_gallons_to_liters():
    result = autounit_convert("1", "gallon", "liter")
    value = extract_value(result)
    assert_float_equal(value, 3.78541, tolerance=0.01)
    assert "liter" in result

# TEST FOR MILLILITERS TO FLUID OUNCES
def test_autounit_convert_milliliters_to_fluid_ounces():
    result = autounit_convert("100", "milliliter", "fluid_ounce")
    value = extract_value(result)
    assert_float_equal(value, 3.3814, tolerance=0.1)
    assert "fluid_ounce" in result

# TESTS FOR WEIGHT CONVERSIONS

# TEST FOR KILOGRAMS TO POUNDS
def test_autounit_convert_kilograms_to_pounds():
    result = autounit_convert("50", "kilogram", "pound")
    value = extract_value(result)
    assert_float_equal(value, 110.231, tolerance=0.1)
    assert "pound" in result

# TEST FOR POUNDS TO KILOGRAMS
def test_autounit_convert_pounds_to_kilograms():
    result = autounit_convert("100", "pound", "kilogram")
    value = extract_value(result)
    assert_float_equal(value, 45.3592, tolerance=0.1)
    assert "kilogram" in result

# TEST FOR GRAMS TO OUNCES
def test_autounit_convert_grams_to_ounces():
    result = autounit_convert("100", "gram", "ounce")
    value = extract_value(result)
    assert_float_equal(value, 3.5274, tolerance=0.01)
    assert "ounce" in result

# TESTS FOR TEMPERATURE CONVERSIONS

# TEST FOR CELSIUS TO FAHRENHEIT
def test_autounit_convert_celsius_to_fahrenheit():
    result = autounit_convert("25", "celsius", "fahrenheit")
    value = extract_value(result)
    assert_float_equal(value, 77, tolerance=0.1)
    assert "fahrenheit" in result

# TEST FOR FAHRENHEIT TO CELSIUS
def test_autounit_convert_fahrenheit_to_celsius():
    result = autounit_convert("77", "fahrenheit", "celsius")
    value = extract_value(result)
    assert_float_equal(value, 25, tolerance=0.1)
    assert "celsius" in result

# TEST FOR CELSIUS TO KELVIN
def test_autounit_convert_celsius_to_kelvin():
    result = autounit_convert("0", "celsius", "kelvin")
    value = extract_value(result)
    assert_float_equal(value, 273.15, tolerance=0.01)
    assert "kelvin" in result

# TEST FOR KELVIN TO CELSIUS
def test_autounit_convert_kelvin_to_celsius():
    result = autounit_convert("273.15", "kelvin", "celsius")
    value = extract_value(result)
    assert_float_equal(value, 0, tolerance=0.01)
    assert "celsius" in result

# TESTS FOR NUMERIC INPUT FORMATS

# TEST FOR INTEGER INPUT
def test_autounit_convert_integer_input():
    result = autounit_convert(100, "meter", "feet")
    value = extract_value(result)
    assert value > 0
    assert "feet" in result

# TEST FOR FLOAT INPUT
def test_autounit_convert_float_input():
    result = autounit_convert(3.14159, "meter", "feet")
    value = extract_value(result)
    assert value > 0
    assert "feet" in result

# TEST FOR STRING WITH COMMAS
def test_autounit_convert_string_with_commas():
    result = autounit_convert("1,000", "meter", "feet")
    value = extract_value(result)
    assert_float_equal(value, 3280.84, tolerance=1)
    assert "feet" in result

# TEST FOR STRING WITH WHITESPACE
def test_autounit_convert_string_with_whitespace():
    result = autounit_convert("  100  ", "meter", "feet")
    value = extract_value(result)
    assert value > 0
    assert "feet" in result

# TESTS FOR ERROR HANDLING

# TEST FOR INVALID VALUE
def test_autounit_convert_invalid_value():
    with pytest.raises(ValueError, match="INVALID VALUE OR UNIT"):
        autounit_convert("invalid", "meter", "feet")

# TEST FOR INCOMPATIBLE UNITS
def test_autounit_convert_incompatible_units():
    with pytest.raises(ValueError, match="CANNOT CONVERT"):
        autounit_convert("100", "meter", "liter")

# TEST FOR INVALID UNIT NAME
def test_autounit_convert_invalid_unit():
    with pytest.raises(ValueError):
        autounit_convert("100", "invalid_unit", "feet")

# TEST FOR ZERO VALUE
def test_autounit_convert_zero_value():
    result = autounit_convert("0", "meter", "feet")
    value = extract_value(result)
    assert value == 0
    assert "feet" in result

# TEST FOR NEGATIVE VALUE
def test_autounit_convert_negative_value():
    result = autounit_convert("-10", "celsius", "fahrenheit")
    value = extract_value(result)
    assert_float_equal(value, 14, tolerance=0.1)
    assert "fahrenheit" in result

# TEST FOR VERY LARGE VALUE
def test_autounit_convert_large_value():
    result = autounit_convert("1000000", "meter", "kilometer")
    value = extract_value(result)
    assert_float_equal(value, 1000, tolerance=0.1)
    assert "kilometer" in result

# TEST FOR VERY SMALL VALUE
def test_autounit_convert_small_value():
    result = autounit_convert("0.001", "meter", "millimeter")
    value = extract_value(result)
    assert_float_equal(value, 1, tolerance=0.01)
    assert "millimeter" in result

# TEST FOR PYPERCLIP EXCEPTION HANDLING
def test_autounit_convert_pyperclip_exception(monkeypatch):
    def mock_copy_fail(text):
        raise pyperclip.PyperclipException("Clipboard error")
    monkeypatch.setattr(pyperclip, "copy", mock_copy_fail)
    result = autounit_convert("100", "meter", "feet")
    assert "feet" in result

# TEST FOR ROUND-TRIP CONVERSIONS
def test_autounit_convert_round_trip():
    original_value = "100"
    result1 = autounit_convert(original_value, "meter", "feet")
    feet_value = extract_value(result1)
    result2 = autounit_convert(str(feet_value), "feet", "meter")
    meter_value = extract_value(result2)
    assert_float_equal(meter_value, float(original_value), tolerance=0.1)

# TEST FOR DIFFERENT UNIT ALIASES
@pytest.mark.parametrize("from_unit,to_unit", [ ("m", "ft"), ("km", "mi"), ("kg", "lb"), ("L", "gal") ])
def test_autounit_convert_unit_aliases(from_unit, to_unit):
    result = autounit_convert("1", from_unit, to_unit)
    assert to_unit in result or any(alias in result for alias in ["feet", "mile", "pound", "gallon"])
