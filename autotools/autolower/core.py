import pyperclip

# TRANSFORMS TEXT TO LOWERCASE AND COPIES IT TO CLIPBOARD
def autolower_transform(text):
    transformed_text = text.lower()
    try: pyperclip.copy(transformed_text)
    except pyperclip.PyperclipException: pass
    return transformed_text
