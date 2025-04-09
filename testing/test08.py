import fitz
import pytest

from website.extractor.structure.resume import Resume


def check_work_experience(resume: Resume):
    work_experience = resume.get_work_experience()
    expected = [['октябрь 2024 года - настоящее время', 'Вконтакте'],
                ['июль 2023 года - октябрь 2024 года', 'Яндекс'],
                ['сентябрь 2022 года - июль 2023 года', 'Центральный банк']]

    for obj, expected_obj in zip(work_experience, expected):
        assert obj.date == expected_obj[0]
        assert expected_obj[1].lower() in obj.orgs.lower()

def check_education(resume: Resume):
    education = resume.get_education()
    expected = [['2026 год', 'НИУ ВШЭ'],
                ['2024 год', 'НИУ ВШЭ']]

    for obj, expected_obj in zip(education, expected):
        assert obj.date == expected_obj[0]
        assert expected_obj[1].lower() in obj.orgs.lower()

def test08():
    doc = fitz.open("testing-pdfs/test08.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        check_work_experience(resume)
        check_education(resume)
    except Exception as e:
        pytest.fail(f"Test 08 failed with error {type(e).__name__}")

    print("Test 08 passed.")
