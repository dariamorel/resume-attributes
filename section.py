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

# Функция для получения детей токена
def get_children(token_id, doc):
    children = []
    for token in doc.tokens:
        if token.head_id == token_id:  # Если токен зависит от текущего
            children.append(token)
    return children

class Section:
    def __init__(self, section_doc: Doc):
        self.__list_of_tokens = list()

        added_words = {i: False for i in range(len(section_doc.tokens))}

        # выделение головных токенов
        head_tokens = [token for token in section_doc.tokens if token.rel == "root"]

        # какому токену какой ent соответствует
        token_to_ent = {i: -1 for i in range(len(section_doc.tokens))}
        for i, ent in enumerate(section_doc.spans):
            for token in ent.tokens:
                token_i = int(token.id[2:]) - 1
                token_to_ent[token_i] = i

        for token in head_tokens:
            token_list = list()
            self.__tokens_division(token, token_list, section_doc, added_words, token_to_ent)
            if token_list:
                self.__list_of_tokens.append(token_list)

    def get_list_of_tokens(self):
        return self.__list_of_tokens


    # private
    def __tokens_division(self, token, token_list: list, section_doc: Doc, added_words, token_to_ent):
        token_i = int(token.id[2:]) - 1

        # слово еще не добавили
        if not added_words[token_i]:
            # если ent и еще не добавлен
            if token_to_ent[token_i] != -1:
                ent = section_doc.spans[token_to_ent[token_i]]
                self.__list_of_tokens.append(ent.text)
                # помечаем, что добавили слово
                for ent_token in ent.tokens:
                    ent_token_i = int(ent_token.id[2:]) - 1
                    added_words[ent_token_i] = True

                # пробегаемся по детям
                for child in get_children(token.id, section_doc):
                    clear_token_list = list()
                    self.__tokens_division(child, clear_token_list, section_doc, added_words, token_to_ent)
                    if clear_token_list:
                        self.__list_of_tokens.append(clear_token_list)
                return

            # если не ent
            token_list.append(token.text)
            # пробегаемся по детям
            for child in get_children(token.id, section_doc):
                self.__tokens_division(child, token_list, section_doc, added_words, token_to_ent)
            return

        # если слово уже добавлено
        # пробегаемся по детям
        for child in get_children(token.id, section_doc):
            clear_token_list = list()
            self.__tokens_division(child, clear_token_list, section_doc, added_words, token_to_ent)
            if clear_token_list:
                self.__list_of_tokens.append(clear_token_list)
        return

class MainInfo(Section):
    pass

class WorkExperience(Section):
    pass

class Education(Section):
    pass

class Skills(Section):
    pass