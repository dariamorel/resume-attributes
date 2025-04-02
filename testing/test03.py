import fitz
import pytest

from website.extractor.structure.resume import Resume

def first():
    doc = fitz.open("testing-pdfs/test03-first.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_name() == "Игорь"
    except Exception as e:
        pytest.fail(f"Test 03 failed with error {type(e).__name__}")

def first_last():
    doc = fitz.open("testing-pdfs/test03-first-last.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_name() == "Давыдов Яков"
    except Exception as e:
        pytest.fail(f"Test 03 failed with error {type(e).__name__}")

def first_last_middle():
    doc = fitz.open("testing-pdfs/test03-first-last-middle.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_name() == "Щекочихина Елена Викторовна"
    except Exception as e:
        pytest.fail(f"Test 03 failed with error {type(e).__name__}")

def with_spaces():
    # Внутри ФИО есть перенос строки и несколько пробелов
    doc = fitz.open("testing-pdfs/test03-with-spaces.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_name() == "Шурыгин Александр Валерьевич"
    except Exception as e:
        pytest.fail(f"Test 03 failed with error {type(e).__name__}")

def test03():
    first()
    first_last()
    first_last_middle()
    with_spaces()

    print("Test 03 passed.")