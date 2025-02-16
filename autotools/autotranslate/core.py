from deep_translator import GoogleTranslator
from langdetect import detect
import pyperclip

def get_supported_languages() -> dict:
    """GET ALL SUPPORTED LANGUAGES FROM GOOGLE TRANSLATE"""
    # GET LANGUAGES CODES
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    # SORT BY LANGUAGE NAME
    return dict(sorted(langs.items(), key=lambda x: x[1].lower()))

def translate_text(text: str, to_lang: str = 'en', from_lang: str = None, 
                  copy: bool = False, detect_lang: bool = False, output: str = None) -> str:
    """TRANSLATE TEXT TO SPECIFIED LANGUAGE
    
    ARGS:
        text (str): TEXT TO TRANSLATE
        to_lang (str): TARGET LANGUAGE CODE (DEFAULT: EN)
        from_lang (str): SOURCE LANGUAGE CODE (DEFAULT: AUTO-DETECT)
        copy (bool): COPY RESULT TO CLIPBOARD
        detect_lang (bool): SHOW DETECTED SOURCE LANGUAGE
        output (str): PATH TO SAVE TRANSLATION TO FILE
        
    RETURNS:
        str: TRANSLATED TEXT
    """
    # AUTO-DETECT SOURCE LANGUAGE IF NOT SPECIFIED
    source_lang = from_lang or detect(text)
    
    # TRANSLATE
    translator = GoogleTranslator(source=source_lang, target=to_lang)
    result = translator.translate(text)
    
    # COPY TO CLIPBOARD IF REQUESTED
    if copy:
        pyperclip.copy(result)
    
    # SAVE TO FILE IF OUTPUT PATH PROVIDED
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as f:
                if detect_lang:
                    f.write(f"[Detected: {source_lang}] {result}")
                else:
                    f.write(result)
        except Exception as e:
            print(f"\nError saving to file: {str(e)}")
    
    # RETURN RESULT WITH DETECTED LANGUAGE IF REQUESTED
    if detect_lang:
        return f"[Detected: {source_lang}] {result}"
    return result 
