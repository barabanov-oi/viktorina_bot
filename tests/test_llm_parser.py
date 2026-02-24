import pytest

from app.llm.parser import parse_llm_question, LLMParseError


def test_parser_ok():
    raw = '{"question":"Q? очень длинный текст","answers":["a","b","c","d"],"correct_index":2,"explanation":"okay","tags":["x"]}'
    dto = parse_llm_question(raw)
    assert dto.correct_index == 2


def test_parser_invalid_json():
    with pytest.raises(LLMParseError):
        parse_llm_question("not-json")
