import pyperclip
from pint import UnitRegistry

# INITIALIZE UNIT REGISTRY
ureg = UnitRegistry()

# CONVERTS MEASUREMENT UNITS
def autounit_convert(value, from_unit, to_unit):
    try:
        if isinstance(value, str):
            value = value.strip()
            value = value.replace(',', '')
        
        value_float = float(value)
        quantity = ureg.Quantity(value_float, from_unit)
        result = quantity.to(to_unit)
        result_value = result.magnitude
        
        if abs(result_value) >= 1000 or abs(result_value) < 0.01: result_str = f"{result_value:.6g}"
        elif abs(result_value) >= 1: result_str = f"{result_value:.4f}".rstrip('0').rstrip('.')
        else: result_str = f"{result_value:.6f}".rstrip('0').rstrip('.')
        
        output = f"{result_str} {to_unit}"
        
        try: pyperclip.copy(output)
        except pyperclip.PyperclipException: pass
        
        return output
    
    except ValueError as e:
        raise ValueError(f"INVALID VALUE OR UNIT: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "cannot convert" in error_msg.lower() or "incompatible" in error_msg.lower():
            raise ValueError(f"CANNOT CONVERT FROM '{from_unit}' TO '{to_unit}': INCOMPATIBLE UNITS")
        raise ValueError(f"CONVERSION ERROR: {error_msg}")
