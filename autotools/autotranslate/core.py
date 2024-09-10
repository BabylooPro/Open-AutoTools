import requests
import os
import pyperclip

# PARAMETERS API
BASE_URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/{}"
HEADERS = {
    "X-RapidAPI-Key": os.getenv('RAPIDAPI_API_KEY'),
    "X-RapidAPI-Host": "google-translate113.p.rapidapi.com"
}


# FUNCTION TO GET SUPPORTED LANGUAGES
def autotranslate_supported_languages():
    endpoint = "support-languages"
    full_url = BASE_URL.format(endpoint)
    response = requests.get(full_url, headers=HEADERS)
    languages = response.json()

    language_codes = [lang['code'] for lang in languages]
    return language_codes


# FUNCTION TO TRANSLATE TEXT AND COPY TO CLIPBOARD
def autotranslate_text(text, language_target):
    endpoint = "text"
    full_url = BASE_URL.format(endpoint)
    payload = {"from": "auto", "to": language_target, "text": text}
    specific_headers = {
        **HEADERS, "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(full_url, data=payload, headers=specific_headers)
    translated_text = response.json()['trans']

    # COPY TRANSLATED TEXT TO CLIPBOARD
    pyperclip.copy(translated_text)

    return translated_text
