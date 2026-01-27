# AutoUnit

## Description

Converts measurement units between different systems (example: meters to feet, liters to gallons) and automatically copies the result to your clipboard.

## Supported Unit Categories

### Length

- **Metric**: meter (m), kilometer (km), centimeter (cm), millimeter (mm)
- **Imperial/US**: feet (ft), inch (in), mile (mi), yard (yd)

### Volume

- **Metric**: liter (L), milliliter (mL)
- **Imperial/US**: gallon (gal), fluid_ounce (fl_oz), cup, pint, quart

### Weight/Mass

- **Metric**: kilogram (kg), gram (g), ton (t)
- **Imperial/US**: pound (lb), ounce (oz), stone

### Temperature

- **Celsius** (°C)
- **Fahrenheit** (°F)
- **Kelvin** (K)

### Additional Units

AutoUnit uses the `pint` library, which supports many more unit categories including:

- Area (square meters, square feet, acres, etc.)
- Speed (meters per second, miles per hour, etc.)
- Energy (joules, calories, BTUs, etc.)
- Pressure (pascal, bar, psi, etc.)
- And many more...

## Usage

```bash
autounit <value> <from_unit> <to_unit>
```

### Arguments

- `value`: The numeric value to convert (supports integers, decimals, and comma-separated numbers)
- `from_unit`: The source unit (e.g., 'meter', 'feet', 'liter', 'gallon')
- `to_unit`: The target unit (e.g., 'meter', 'feet', 'liter', 'gallon')

## Examples

### Length Conversions

```bash
# Convert meters to feet
autounit 100 meter feet
# Output: 328.084 feet

# Convert kilometers to miles
autounit 1 kilometer mile
# Output: 0.621371 mile

# Convert inches to centimeters
autounit 1 inch centimeter
# Output: 2.54 centimeter
```

### Volume Conversions

```bash
# Convert liters to gallons
autounit 10 liter gallon
# Output: 2.64172 gallon

# Convert gallons to liters
autounit 1 gallon liter
# Output: 3.78541 liter

# Convert milliliters to fluid ounces
autounit 100 milliliter fluid_ounce
# Output: 3.3814 fluid_ounce
```

### Weight Conversions

```bash
# Convert kilograms to pounds
autounit 50 kilogram pound
# Output: 110.231 pound

# Convert pounds to kilograms
autounit 100 pound kilogram
# Output: 45.3592 kilogram

# Convert grams to ounces
autounit 100 gram ounce
# Output: 3.5274 ounce
```

### Temperature Conversions

```bash
# Convert Celsius to Fahrenheit
autounit 25 celsius fahrenheit
# Output: 77 fahrenheit

# Convert Fahrenheit to Celsius
autounit 77 fahrenheit celsius
# Output: 25 celsius

# Convert Celsius to Kelvin
autounit 0 celsius kelvin
# Output: 273.15 kelvin

# Convert Kelvin to Celsius
autounit 273.15 kelvin celsius
# Output: 0 celsius
```

### Using Unit Aliases

```bash
# Short unit names work too
autounit 1 m ft
autounit 1 km mi
autounit 1 kg lb
autounit 1 L gal
```

### Numeric Format Support

```bash
# Comma-separated numbers
autounit 1,000 meter feet
# Output: 3280.84 feet

# Decimal values
autounit 3.14159 meter feet
# Output: 10.3084 feet

# Negative values (useful for temperature)
autounit -10 celsius fahrenheit
# Output: 14 fahrenheit
```

## Notes

- The converted value is automatically copied to your clipboard
- Unit names are case-insensitive (meter, Meter, METER all work)
- Supports both full unit names and common abbreviations (m, ft, kg, lb, etc.)
- Values can include commas for thousands separators
- Whitespace around values is automatically trimmed
- Results are formatted with appropriate precision based on the magnitude of the value
- Cannot convert between incompatible unit categories (e.g., length to volume)
- Uses the `pint` library for unit conversions, which supports a wide variety of units beyond the examples shown

## Error Handling

- **Invalid value**: If the value cannot be parsed as a number, an error will be displayed
- **Incompatible units**: If attempting to convert between incompatible unit categories (e.g., meters to liters), an error will be displayed
- **Invalid unit**: If a unit name is not recognized, an error will be displayed
