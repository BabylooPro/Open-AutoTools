import requests
import os

# AUTOCAPS FUNCTION DEFINITION
def autocorrect_text(text, language="en"):
    # API CALL TO REWRITER API
    url = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

    # PAYLOAD AND HEADERS FOR API CALL
    payload = {
        "language": language,
        "strength": 3, # STRENGTH OF REWRITING (STRENGTH 3 IS RECOMMENDED FOR BETTER RESULTS)
        "text": text
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_REWRITER_API_KEY'), # API KEY FROM ENVIRONMENT VARIABLE
        "X-RapidAPI-Host": "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com"
    }

    # RESPONSE FROM API CALL
    response = requests.post(url, json=payload, headers=headers)

    # RETURN REWRITTEN TEXT IF SUCCESSFUL ELSE RETURN ERROR MESSAGE
    if response.status_code == 200:
        return response.json()['rewrite']
    else:
        return "ERROR: CORRECTION FAILED - " + response.text + response.status_code
