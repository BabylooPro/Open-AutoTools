import pyperclip

# TRANSFORMS TEXT TO UPPERCASE AND COPIES IT TO CLIPBOARD
def autocaps_transform(text):
    transformed_text = text.upper()
    try: pyperclip.copy(transformed_text)
    except pyperclip.PyperclipException: pass 
    return transformed_text
