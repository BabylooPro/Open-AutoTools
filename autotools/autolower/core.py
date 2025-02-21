import pyperclip

# AUTOLOWERCASE CORE FUNCTION DEFINITION
def autolower_transform(text):
    transformed_text = text.lower()  # TRANSFORM TEXT TO LOWERCASE
    try:
        pyperclip.copy(transformed_text)  # COPY TRANSFORMED TEXT TO CLIPBOARD
    except pyperclip.PyperclipException:
        pass  # IGNORE CLIPBOARD ERRORS IN HEADLESS ENVIRONMENT
    return transformed_text
