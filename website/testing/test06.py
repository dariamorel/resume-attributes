import fitz
import pytest

from website.extractor.structure.resume import Resume

def comma():
    doc = fitz.open("testing-pdfs/test06-comma.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        skills = resume.get_skills()
        expected = ["Продажи", "Сопровождение ключевых клиентов", "SMM", "Публичные выступления и презентации"]
        assert len(skills) == len(expected)
        for skill, expected_skill in zip(skills, expected):
            assert skill == expected_skill
    except Exception as e:
        pytest.fail(f"Test 06 failed with error {type(e).__name__}")

def whitespace():
    doc = fitz.open("testing-pdfs/test06-whitespace.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        skills = resume.get_skills()
        expected = ["REST", "SOAP", "API", "JSON","UML", "BPMN", "Atlassian Confluence", "Atlassian Jira", "Figma", "Miro", "Kibana"]
        assert len(skills) == len(expected)
        for skill, expected_skill in zip(skills, expected):
            assert skill == expected_skill
    except Exception as e:
        pytest.fail(f"Test 06 failed with error {type(e).__name__}")

def test06():
    comma()
    whitespace()

    print("Test 06 passed.")