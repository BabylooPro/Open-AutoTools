import pyperclip

# AUTOCAPS CORE FUNCTION DEFINITION
def autocaps_transform(text):
    transformed_text = text.upper()  # TRANSFORM TEXT TO UPPERCASE
    try:
        pyperclip.copy(transformed_text)  # COPY TRANSFORMED TEXT TO CLIPBOARD
    except pyperclip.PyperclipException:
        pass  # IGNORE CLIPBOARD ERRORS IN HEADLESS ENVIRONMENT
    return transformed_text
