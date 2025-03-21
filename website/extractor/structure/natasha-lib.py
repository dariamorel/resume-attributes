import re

import fitz

from resume import Resume, clean_text
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    NamesExtractor,
    DatesExtractor,
    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)


def main():
    # file = open("test.txt", "r")
    # text = file.read()

    resume_names = ['test.pdf', 'Perl-программист.pdf', 'марина_лалала_резюме.pdf', 'Михаил Васильев.pdf',
                    'Резюме Junior Python Developer.pdf', 'Резюме Юрист.pdf']
    # for name in resume_names:
    pdf_path = f"/home/daria/курсач/выборка/{resume_names[1]}"
    pdf_doc = fitz.open(pdf_path)
    all_text = ""
    for page in pdf_doc:
        all_text += page.get_text()

    text = all_text
    # print(text)

    resume = Resume(text)
    work_experience = resume.get_work_experience()
    # # for obj in work_experience.get_info():
    # #     print(obj.text)
    for span in work_experience.spans:
        print(span.text)

# def main2(text):
#     file = open("test.txt", "r")
#     text = file.read()

if __name__ == "__main__":
    main()