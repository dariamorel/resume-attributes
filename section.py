from natasha import (Doc)
from document import Document

class Section:
    def __init__(self, section_doc: Document):
        """
        :param section_doc: Document
        """
        self.__list_of_tokens = list()

        added_words = {i: False for i in range(len(section_doc.tokens))}

        # выделение головных токенов
        head_tokens = [token for token in section_doc.tokens if token.rel == "root"]

        # какому токену какой ent соответствует
        token_to_ent = {i: -1 for i in range(len(section_doc.tokens))}
        for i, ent in enumerate(section_doc.spans):
            for token in ent.tokens:
                token_to_ent[token.i] = i

        for token in head_tokens:
            token_list = list()
            self.__tokens_division(token, token_list, section_doc, added_words, token_to_ent)
            if token_list:
                self.__list_of_tokens.append(token_list)

    def get_list_of_tokens(self):
        return self.__list_of_tokens


    # private
    def __tokens_division(self, token, token_list: list, section_doc: Doc, added_words, token_to_ent):
        # слово еще не добавили
        if not added_words[token.i]:
            # если ent и еще не добавлен
            if token_to_ent[token.i] != -1:
                ent = section_doc.spans[token_to_ent[token.i]]
                self.__list_of_tokens.append(ent.text)
                # помечаем, что добавили слово
                for ent_token in ent.tokens:
                    added_words[ent_token.i] = True

                # пробегаемся по детям
                for child in token.children:
                    clear_token_list = list()
                    self.__tokens_division(child, clear_token_list, section_doc, added_words, token_to_ent)
                    if clear_token_list:
                        self.__list_of_tokens.append(clear_token_list)
                return

            # если не ent
            token_list.append(token.text)
            # пробегаемся по детям
            for child in token.children:
                self.__tokens_division(child, token_list, section_doc, added_words, token_to_ent)
            return

        # если слово уже добавлено
        # пробегаемся по детям
        for child in token.children:
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