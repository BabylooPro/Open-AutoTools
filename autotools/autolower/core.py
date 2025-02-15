import pyperclip

# AUTOLOWERCASE CORE FUNCTION DEFINITION
def autolower_transform(text):
    transformed_text = text.lower()  # TRANSFORM TEXT TO LOWERCASE
    pyperclip.copy(transformed_text)  # COPY TRANSFORMED TEXT TO CLIPBOARD
    return transformed_text
