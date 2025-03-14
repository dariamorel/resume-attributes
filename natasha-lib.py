import re
import time

import fitz
import natasha

from resume import Resume
from section import Section
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,
    DatesExtractor,

    Doc
)
from document import Word, Document, Date
from natasha.extractors import Match

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


from resume import sections_dict


def main():
    from natasha import obj

    file = open("test.txt", "r")
    text = file.read()

    # pdf_path = "/home/daria/курсач/резюме/Perl-программист.pdf"
    # pdf_doc = fitz.open(pdf_path)
    # all_text = ""
    # for page in pdf_doc:
    #     all_text += page.get_text()
    #
    # text = all_text.replace("\n", ", ").replace(".", ",")
    # print(text)

    # cur_time = time.time()
    resume = Resume(text)
    ed = resume.get_education()
    for obj in ed.get_info():
        print(obj.text)
    # print(time.time() - cur_time)


if __name__ == "__main__":
    main()