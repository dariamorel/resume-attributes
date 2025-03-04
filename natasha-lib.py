import re
import fitz
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

# Функция для получения детей токена
def get_children(token_id, doc):
    children = []
    for token in doc.tokens:
        if token.head_id == token_id:  # Если токен зависит от текущего
            children.append(token)
    return children


# pdf_path = "/home/daria/курсач/резюме/Perl-программист.pdf"
# pdf_doc = fitz.open(pdf_path)
# all_text = ""
# for page in pdf_doc:
#     all_text += page.get_text()

#print(all_text)

file = open("test.txt", "r")
text = file.read()
cleaned_text = clean_text(text)

resume = Resume(cleaned_text)

education_doc = resume.get_main_info()
section = Section(education_doc)
for token in section.get_list_of_tokens():
    print(token)