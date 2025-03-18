import re

import fitz

from .resume import Resume
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    NamesExtractor,
    DatesExtractor
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)


def clean_text(input_text):
    cleaned_input = re.sub(r'[.,?!]', '', input_text)
    return cleaned_input


def main():
    # file = open("test.txt", "r")
    # text = file.read()

    pdf_path = "/home/daria/курсач/резюме/test.pdf"
    pdf_doc = fitz.open(pdf_path)
    all_text = ""
    for page in pdf_doc:
        all_text += page.get_text()

    text = all_text
    # print(text)

    resume = Resume(text)
    main_info = resume.get_main_info()
    print(main_info.email.text)
    # for obj in main_info:
    #     print(obj.text)
    # ed = resume.get_main_info()
    # for obj in ed.get_info():
    #     if obj:
    #         print(obj.text)


if __name__ == "__main__":
    main()