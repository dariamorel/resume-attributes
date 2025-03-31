import fitz
import pytest

from website.extractor.structure.resume import Resume

def check():
    doc = fitz.open("testing-pdfs/test07.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        languages = resume.get_languages()
        expected = [["Русский", "Родной"], ["Английский", "C2"], ["Немецкий", "B1"]]
        assert len(languages) == len(expected)
        for lang, expected_lang in zip(languages, expected):
            assert lang.name == expected_lang[0]
            assert lang.info == expected_lang[1]
    except Exception as e:
        pytest.fail(f"Test 07 failed with error {type(e).__name__}")

def test07():
    check()

    print("Test 07 passed.")