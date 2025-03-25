import re
import time
import spacy
import yake

import fitz

from resume import Resume
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
                    'Резюме_Судакова_Виталия_.pdf', 'РЕЗЮМЕ_Мошенко (1).pdf',
                    'Резюме_Системныи_аналитик_Илья_Губин.pdf', 'резюме_Земцов.pdf',
                    'Резюме_Event_менеджер_Е_Щекочихина.pdf', 'Яков Давыдов_CV.pdf', 'Лебедева А.С. Резюме.pdf',
                    'CV Ангелина.pdf', 'CV_Chizhik_jan2025.pdf', 'CV Shitikova.pdf', 'Громов резюме (1).pdf',
                    'Резюме_Аракелян_Адриана_Артуровна_Юрист_помощник_юриста.pdf']
    # for name in resume_names:
    pdf_path = f"/home/daria/курсач/выборка/{resume_names[3]}"
    pdf_doc = fitz.open(pdf_path)
    all_text = ""
    for page in pdf_doc:
        all_text += page.get_text()

    text = all_text
    # print(text)

    resume = Resume(text)
    print(resume.languages.languages)

    # for obj in resume.skills.objects:
    #     print(obj.text)


def main2():
    text = "python js языки английский"
    groups = re.search(rf'(навыки)(.*?)(языки|\Z)', text,
                       re.DOTALL | re.IGNORECASE)
    print(groups.group(2))

if __name__ == "__main__":
    main()
