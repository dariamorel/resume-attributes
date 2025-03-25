import re
import time
import spacy

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
                    'Резюме_Судакова_Виталия_.pdf', 'РЕЗЮМЕ_Мошенко (1).pdf',
                    'Резюме_Системныи_аналитик_Илья_Губин.pdf', 'резюме_Земцов.pdf',
                    'Резюме_Event_менеджер_Е_Щекочихина.pdf', 'Яков Давыдов_CV.pdf', 'Лебедева А.С. Резюме.pdf',
                    'CV Ангелина.pdf', 'CV_Chizhik_jan2025.pdf', 'CV Shitikova.pdf', 'Громов резюме (1).pdf',
                    'Резюме_Аракелян_Адриана_Артуровна_Юрист_помощник_юриста.pdf']
    # for name in resume_names:
    pdf_path = f"/home/daria/курсач/выборка/{resume_names[1]}"
    pdf_doc = fitz.open(pdf_path)
    all_text = ""
    for page in pdf_doc:
        all_text += page.get_text()

    text = all_text
    # print(text)

    resume = Resume(text)
    for obj in resume.work_experience.objects:
        print(obj.text)
    # # print(resume.main_info)
    # print(resume.position)
    # print(resume.work_experience)
    # print(resume.education)
    # print(resume.courses)
    # print(resume.projects)
    # print(resume.achievements)
    # print(resume.skills)
    # print(resume.languages)


def main2():
    text = "привет опыт: раз два три проекты навыки"
    groups = re.findall(rf'(опыт(\s|:))(.*?)(навыки|проекты|\Z)', text,
                       re.DOTALL | re.IGNORECASE)
    section = max((group[2] for group in groups), key=len)
    print(groups)

if __name__ == "__main__":
    main()
