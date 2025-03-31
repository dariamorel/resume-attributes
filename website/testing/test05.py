import fitz
import pytest
from natasha import Doc, Segmenter, NewsEmbedding, NewsMorphTagger, MorphVocab
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
morph_vocab = MorphVocab()

from website.extractor.structure.resume import Resume

def lemmatize(text):
    doc = Doc(text.lower())
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    lemmatized_text = ""
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        lemmatized_text += token.lemma + ' '
    return lemmatized_text.strip()

def section_position():
    doc = fitz.open("testing-pdfs/test05-section-position.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        position = resume.get_position()
        assert position[0] == 'Perl-программист.'
        assert position[1] == 'Программист.'
        assert position[2] == 'Разработчик.'
        assert len(position) == 3

    except Exception as e:
        pytest.fail(f"Test 05 failed with error {type(e).__name__}")

def no_section_position():
    doc = fitz.open("testing-pdfs/test05-no-section-position.pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    try:
        resume = Resume(text)
        # Секция position не найдена
        assert resume.position.text == ""

        # Отражают ли найденные ключевые слова должность
        position = resume.get_position()
        for obj in position:
            # Проверяем совпадения для всех форм слов
            assert any([lemmatize(sent) in lemmatize(obj) for sent in ["senior software engineer", "software engineer", "высоконагруженные системы", "программист"]])

    except Exception as e:
        pytest.fail(f"Test 05 failed with error {type(e).__name__}")

def test05():
    section_position()
    no_section_position()

    print("Test 05 passed.")