import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple

# CONVERTS TEXT TO JSON FORMAT
def text_to_json(text: str, indent: int = 2) -> str:
    data = {"text": text}
    return json.dumps(data, indent=indent, ensure_ascii=False)

# CONVERTS TEXT TO XML FORMAT
def text_to_xml(text: str, root_tag: str = "text") -> str:
    root = ET.Element(root_tag)
    root.text = text
    return ET.tostring(root, encoding='unicode')

# CONVERTS TEXT TO HTML FORMAT
def text_to_html(text: str, title: str = "Document") -> str:
    escaped_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <pre>{escaped_text}</pre>
</body>
</html>"""

# CONVERTS TEXT TO MARKDOWN FORMAT
def text_to_markdown(text: str) -> str:
    return text

# CONVERTS JSON TO TEXT
def json_to_text(json_str: str) -> str:
    try:
        data = json.loads(json_str)
        if isinstance(data, dict) and "text" in data: return str(data["text"])
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return json_str

# CONVERTS XML TO TEXT
def xml_to_text(xml_str: str) -> str:
    try:
        root = ET.fromstring(xml_str)
        text_parts = []

        for elem in root.iter():
            if elem.text and elem.text.strip(): text_parts.append(elem.text.strip())
            if elem.tail and elem.tail.strip(): text_parts.append(elem.tail.strip())

        result = " ".join(text_parts)
        return result
    except ET.ParseError:
        return xml_str

# CONVERTS TEXT FILE FROM ONE FORMAT TO ANOTHER
def convert_text_file(input_path: str, output_path: str) -> Tuple[bool, str]:
    if not os.path.exists(input_path): raise FileNotFoundError(f"INPUT FILE NOT FOUND: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f: content = f.read()
    
    input_ext = Path(input_path).suffix[1:].lower()
    output_ext = Path(output_path).suffix[1:].lower()
    
    # CONVERT BASED ON INPUT FORMAT
    if input_ext == 'json':
        content = json_to_text(content)
    elif input_ext == 'xml':
        content = xml_to_text(content)
    elif input_ext in ['html', 'htm']:
        from html.parser import HTMLParser
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
            def handle_data(self, data):
                self.text.append(data)
        parser = TextExtractor()
        parser.feed(content)
        content = ' '.join(parser.text)
    
    # CONVERT TO OUTPUT FORMAT
    if output_ext == 'json': content = text_to_json(content)
    elif output_ext == 'xml': content = text_to_xml(content)
    elif output_ext in ['html', 'htm']: content = text_to_html(content)
    
    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        try: os.makedirs(output_dir, exist_ok=True)
        except OSError as e: return False, f"CONVERSION FAILED: Cannot create output directory: {str(e)}"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f: f.write(content)
    except OSError as e:
        return False, f"CONVERSION FAILED: Cannot write output file: {str(e)}"
    
    return True, f"TEXT CONVERTED FROM {input_ext.upper()} TO {output_ext.upper()}"
