import fitz
import pytest

from website.extractor.structure.resume import Resume

def no_section_position():
    # В резюме отсутствует секция "Должность"
    doc = fitz.open("testing-pdfs/test01-without-position.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_position() is not None
    except Exception as e:
        pytest.fail(f"Test 01 failed with error {type(e).__name__}")

def no_section_work_experience():
    # В резюме отсутствует секция "Опыт работы"
    doc = fitz.open("testing-pdfs/test01-without-work-experience.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_work_experience() is None
    except Exception as e:
        pytest.fail(f"Test 01 failed with error {type(e).__name__}")

def no_section_education():
    # В резюме отсутствует секция "Образование"
    doc = fitz.open("testing-pdfs/test01-without-education.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_education() is None
    except Exception as e:
        pytest.fail(f"Test 01 failed with error {type(e).__name__}")

def no_section_skills():
    # В резюме отсутствует секция "Навыки"
    doc = fitz.open("testing-pdfs/test01-without-skills.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_skills() is None
    except Exception as e:
        pytest.fail(f"Test 01 failed with error {type(e).__name__}")

def no_section_languages():
    # В резюме отсутствует секция "Языки"
    doc = fitz.open("testing-pdfs/test01-without-languages.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_languages() is None
    except Exception as e:
        pytest.fail(f"Test 01 failed with error {type(e).__name__}")

def test01():
    no_section_position()
    no_section_work_experience()
    no_section_education()
    no_section_skills()
    no_section_languages()

    print("Test 01 passed.")