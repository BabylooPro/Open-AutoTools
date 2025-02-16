import language_tool_python
import spacy
from typing import List, Dict, Optional
import pyperclip
import requests
from langdetect import detect, detect_langs

class SpellChecker:
    def __init__(self):
        # INITIALIZE LANGUAGE TOOL
        self.tool = language_tool_python.LanguageTool('auto')
        
        # CACHE FOR SPACY MODELS
        self.nlp_models = {}

    # LOAD SPACY MODEL FOR GIVEN LANGUAGE
    def _load_spacy_model(self, lang_code: str) -> Optional[spacy.language.Language]:
        """LOAD SPACY MODEL FOR GIVEN LANGUAGE"""
        try:
            if lang_code not in self.nlp_models:
                # GET ALL INSTALLED MODELS FOR THIS LANGUAGE
                available_models = [
                    model for model in spacy.util.get_installed_models()
                    if model.startswith(lang_code)
                ]
                
                if not available_models:
                    # TRY TO CREATE A BLANK MODEL IF NO TRAINED MODELS
                    self.nlp_models[lang_code] = spacy.blank(lang_code)
                else:
                    # USE MOST COMPREHENSIVE MODEL (USUALLY ENDS WITH 'lg' OR 'trf')
                    preferred_model = None
                    for suffix in ['trf', 'lg', 'md', 'sm']:
                        for model in available_models:
                            if model.endswith(suffix):
                                preferred_model = model
                                break
                        if preferred_model:
                            break
                    
                    # IF NO PREFERRED MODEL, USE FIRST AVAILABLE MODEL
                    if not preferred_model:
                        preferred_model = available_models[0]
                    
                    self.nlp_models[lang_code] = spacy.load(preferred_model) # LOAD PREFERRED MODEL
                    
            return self.nlp_models.get(lang_code) # RETURN LOADED MODEL
        except:
            return None

    # CHECK TEXT FOR SPELLING AND GRAMMAR ERRORS
    def check_text(self, text: str, lang: str = 'auto') -> Dict:
        """CHECK TEXT FOR SPELLING AND GRAMMAR ERRORS
        
        ARGS:
            text: Text to check
            lang: Language code (auto for automatic detection)
            
        RETURNS:
            Dict with corrections and statistics
        """
        # DETECT LANGUAGE CONFIDENCE
        if lang == 'auto':
            try:
                lang_scores = detect_langs(text)
                lang = lang_scores[0].lang
                confidence = lang_scores[0].prob
            except:
                confidence = 0
        else:
            confidence = 1.0
            
        # SET LANGUAGE
        if lang != 'auto':
            self.tool.language = lang
            
        # GET MATCHES
        matches = self.tool.check(text)
        
        # PREPARE CORRECTIONS WITH SEVERITY LEVELS
        corrections = []
        for match in matches:
            severity = self._get_error_severity(match)
            correction = {
                'message': match.message,
                'context': match.context,
                'offset': match.offset,
                'length': match.errorLength,
                'category': match.category,
                'rule_id': match.ruleId,
                'replacements': match.replacements,
                'severity': severity
            }
            corrections.append(correction)
            
        # GET DETAILED STATISTICS
        stats = self._get_detailed_stats(corrections)
        
        return {
            'corrections': corrections,
            'statistics': stats,
            'language': {
                'code': lang,
                'name': lang.upper(),
                'confidence': confidence
            }
        }

    # DETERMINE ERROR SEVERITY LEVEL
    def _get_error_severity(self, match) -> str:
        """DETERMINE ERROR SEVERITY LEVEL"""
        if 'TYPO' in match.ruleId or 'SPELLING' in match.ruleId:
            return 'high'
        elif 'GRAMMAR' in match.ruleId:
            return 'medium'
        else:
            return 'low'

    # GET DETAILED ERROR STATISTICS
    def _get_detailed_stats(self, corrections: List[Dict]) -> Dict:
        """GET DETAILED ERROR STATISTICS"""
        stats = {
            'total_errors': len(corrections),
            'categories': {},
            'severity': {
                'high': 0,
                'medium': 0,
                'low': 0
            }
        }
        
        # COUNT ERRORS BY CATEGORY AND SEVERITY
        for corr in corrections:
            # COUNT BY CATEGORY
            cat = corr['category']
            stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
            
            # COUNT BY SEVERITY
            stats['severity'][corr['severity']] += 1
            
        return stats

    # FIX TEXT AUTOMATICALLY
    def fix_text(self, text: str, lang: str = 'auto', copy_to_clipboard: bool = False,
                 ignore: list = None, interactive: bool = False) -> str:
        """FIX TEXT AUTOMATICALLY"""
        if lang != 'auto':
            self.tool.language = lang
        
        if interactive:
            # GET ALL CORRECTIONS
            matches = self.tool.check(text)
            corrected = text
            
            # ASK FOR EACH CORRECTION
            for match in matches:
                if ignore and any(t in match.ruleId.lower() for t in ignore):
                    continue
                    
                print(f"\nError: {match.message}")
                print(f"Context: {match.context}")
                if match.replacements:
                    print("Suggestions:")
                    for i, sugg in enumerate(match.replacements[:3], 1):
                        print(f"{i}. {sugg}")
                        
                    # ASK FOR EACH CORRECTION
                    choice = input("\nApply correction? (1-3/n): ").lower()
                    if choice.isdigit() and 1 <= int(choice) <= len(match.replacements[:3]):
                        replacement = match.replacements[int(choice)-1]
                        corrected = corrected[:match.offset] + replacement + corrected[match.offset + match.errorLength:]
        else:
            # NORMAL AUTO-FIX
            corrected = self.tool.correct(text)
        
        # COPY TO CLIPBOARD IF REQUESTED
        if copy_to_clipboard:
            pyperclip.copy(corrected)
            
        return corrected

    # GET LIST OF SUPPORTED LANGUAGES
    def get_supported_languages(self) -> List[Dict]:
        """GET LIST OF SUPPORTED LANGUAGES"""
        try:
            # GET LANGUAGES FROM LANGUAGE TOOL PUBLIC API
            response = requests.get('https://api.languagetool.org/v2/languages')
            languages = response.json()
            
            # FORMAT LANGUAGES INTO REQUIRED STRUCTURE
            formatted_langs = []
            seen_codes = set()
            
            # FORMAT LANGUAGES INTO REQUIRED STRUCTURE
            for lang in languages:
                code = lang['longCode'].split('-')[0]
                
                # SKIP DUPLICATES
                if code in seen_codes:
                    continue
                    
                # TEST IF LANGUAGE IS ACTUALLY SUPPORTED BY LOCAL TOOL
                try:
                    self.tool.language = code
                    formatted_langs.append({
                        'code': code,
                        'name': lang['name'],
                        'variants': [v['name'] for v in lang.get('variants', [])]
                    })
                    seen_codes.add(code)
                except:
                    continue
            
            return formatted_langs
            
        except Exception as e:
            # IF API FAILS, GET LANGUAGES FROM LOCAL TOOL
            try:
                current_lang = self.tool.language
                return [{'code': current_lang, 'name': current_lang.upper(), 'variants': []}]
            except:
                return []
