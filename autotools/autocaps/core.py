import pyperclip

# AUTOCAPS CORE FUNCTION DEFINITION
def autocaps_transform(text):
    transformed_text = text.upper()  # TRANSFORM TEXT TO UPPERCASE
    pyperclip.copy(transformed_text)  # COPY TRANSFORMED TEXT TO CLIPBOARD
    return transformed_text