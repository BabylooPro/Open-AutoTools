import json
from autotools.autoconvert.conversion.convert_text import (text_to_json, text_to_xml, text_to_html, text_to_markdown, json_to_text, xml_to_text)

# TEXT CONVERSION TESTS

# TEST TEXT TO JSON
def test_text_to_json_basic():
    result = text_to_json("hello world")
    data = json.loads(result)
    assert data["text"] == "hello world"
    assert isinstance(data, dict)

# TEST TEXT TO JSON WITH INDENT
def test_text_to_json_indent():
    result = text_to_json("test", indent=4)
    assert "    " in result

# TEST TEXT TO XML
def test_text_to_xml_basic():
    result = text_to_xml("hello world")
    assert "<text>hello world</text>" in result or "hello world" in result

# TEST TEXT TO XML WITH CUSTOM ROOT TAG
def test_text_to_xml_custom_tag():
    result = text_to_xml("test", root_tag="document")
    assert "document" in result

# TEST TEXT TO HTML
def test_text_to_html_basic():
    result = text_to_html("hello world")
    assert "<!DOCTYPE html>" in result
    assert "<html>" in result
    assert "hello world" in result

# TEST TEXT TO HTML WITH TITLE
def test_text_to_html_with_title():
    result = text_to_html("test", title="My Title")
    assert "My Title" in result

# TEST TEXT TO HTML ESCAPING
def test_text_to_html_escaping():
    result = text_to_html("test <script>alert('xss')</script>")
    assert "&lt;" in result
    assert "&gt;" in result

# TEST TEXT TO MARKDOWN
def test_text_to_markdown():
    result = text_to_markdown("hello world")
    assert result == "hello world"

# TEST JSON TO TEXT
def test_json_to_text_basic():
    json_str = '{"text": "hello world"}'
    result = json_to_text(json_str)
    assert result == "hello world"

# TEST JSON TO TEXT WITH COMPLEX DATA
def test_json_to_text_complex():
    json_str = '{"name": "test", "value": 123}'
    result = json_to_text(json_str)
    assert "test" in result or "123" in result

# TEST JSON TO TEXT WITH INVALID JSON
def test_json_to_text_invalid():
    invalid_json = "not a json"
    result = json_to_text(invalid_json)
    assert result == invalid_json

# TEST XML TO TEXT
def test_xml_to_text_basic():
    xml_str = "<text>hello world</text>"
    result = xml_to_text(xml_str)
    assert result == "hello world"

# TEST XML TO TEXT WITH COMPLEX STRUCTURE
def test_xml_to_text_complex():
    xml_str = "<root><text>test content</text></root>"
    result = xml_to_text(xml_str)
    assert "test content" in result

# TEST XML TO TEXT WITH INVALID XML
def test_xml_to_text_invalid():
    invalid_xml = "<unclosed>tag"
    result = xml_to_text(invalid_xml)
    assert isinstance(result, str)

# TEST XML TO TEXT WITH TAIL
def test_xml_to_text_with_tail():
    xml_str = "<root>text1<child>text2</child>tail</root>"
    result = xml_to_text(xml_str)
    assert "text1" in result
    assert "text2" in result
    assert "tail" in result
