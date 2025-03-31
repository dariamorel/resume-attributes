import fitz
import pytest

from website.extractor.structure.resume import Resume

def phone_email():
    doc = fitz.open("testing-pdfs/test04-phone-email.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_phone_number() == "+7 (965) 298-51-34"
        assert resume.get_email() == "vita.a.sudakova@gmail.com"
        assert resume.get_website() is None
    except Exception as e:
        pytest.fail(f"Test 04 failed with error {type(e).__name__}")

def email_website():
    doc = fitz.open("testing-pdfs/test04-email-website.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_phone_number() is None
        assert resume.get_email() == "tralala@gmail.com"
        assert resume.get_website() == "github.com/lalala"
    except Exception as e:
        pytest.fail(f"Test 04 failed with error {type(e).__name__}")

def phone_email_website():
    doc = fitz.open("testing-pdfs/test04-phone-email-website.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        assert resume.get_phone_number() == "+7 (967) 474-91-48"
        assert resume.get_email() == "VASILYEV.MIKHAIL@GMAIL.COM"
        assert resume.get_website() == "WWW.LINKEDIN.COM/IN/VASILYEVMIKHAIL/"
    except Exception as e:
        pytest.fail(f"Test 04 failed with error {type(e).__name__}")

def test04():
    phone_email()
    email_website()
    phone_email_website()

    print("Test 04 passed.")