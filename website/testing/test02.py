import fitz
import pytest

from website.extractor.structure.resume import Resume

def check_main_info(resume: Resume):
    # Проверка секции main_info
    main_info = resume.main_info
    assert main_info is not None
    text = main_info.text
    assert text[:10] == "Губин Илья"
    assert text[-21:] == "готов к командировкам"

def check_position(resume: Resume):
    # Проверка секции position
    position = resume.position
    assert position is not None
    text = position.text
    assert text[:18] == "Системный аналитик"
    assert text[-17:] == "не имеет значения"

def check_work_experience(resume: Resume):
    # Проверка секции work_experience
    work_experience = resume.work_experience
    assert work_experience is not None
    text = work_experience.text
    assert text[:18] == "— 4 года 5 месяцев"
    assert text[-28:] == "Онбординг новых сотрудников."

def check_education(resume: Resume):
    # Проверка секции education
    education = resume.education
    assert education is not None
    text = education.text
    assert text[:19] == "Среднее специальное"
    assert text[-6:] == "Техник"

def check_skills(resume: Resume):
    # Проверка секции skills
    skills = resume.skills
    assert skills is not None
    text = skills.text
    assert text[:4] == "REST"
    assert text[-6:] == "Kibana"

def check_languages(resume: Resume):
    # Проверка секции languages
    languages = resume.languages
    assert languages is not None
    text = languages.text
    assert text[:7] == "Русский"
    assert text[-7:] == "Средний"


def test02():
    doc = fitz.open("testing-pdfs/test02.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        check_main_info(resume)
        check_position(resume)
        check_work_experience(resume)
        check_education(resume)
        check_skills(resume)
        check_skills(resume)
    except Exception as e:
        pytest.fail(f"Test 02 failed with error {type(e).__name__}")

    print("Test 02 passed.")
