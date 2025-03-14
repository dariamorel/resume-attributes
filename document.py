import natasha


class Word(natasha.doc.DocToken):
    def __init__(self, token: natasha.doc.DocToken):
        super().__init__(token.start, token.stop, token.text, token.id, token.head_id, token.rel, token.pos,
                         token.feats, token.lemma)
        self.head = None
        self.children = None

    @property
    def i(self):
        """  
        :return: индекс слова в предложении  
        """
        return int(self.id.split('_')[1]) - 1

    @property
    def head_i(self):
        """  
        :return: индекс родителя слова в предложении  
        """
        return int(self.head_id.split('_')[1]) - 1


class Document(natasha.doc.Doc):
    def __init__(self, doc: natasha.doc.Doc):
        if doc.tokens is None or doc.spans is None or doc.sents is None:
            ValueError("Not enough data for doc.")
        super().__init__(doc.text, doc.tokens, doc.spans, doc.sents)

        self.tokens = self.__word_tokens(self.tokens)

        self.__word_spans(self.spans)

        self.__word_sents(self.sents)

        self.__add_children()

        self.__add_head()

    def __word_tokens(self, tokens: list):
        """  
        :param tokens: лист токенов типа natasha.doc.DocToken
        :return: лист токенов типа Word
        """
        token_list = [Word(token) for token in tokens]
        return token_list

    def __word_spans(self, spans: list):
        """  
        :param spans: лист spans
        :return: отформатированный лист spans, где вместо DocToken стоит Word
        """
        for span in spans:
            if span.tokens is None:
                ValueError("No tokens in span.")
            span.tokens = self.__word_tokens(span.tokens)
        return spans

    def __word_sents(self, sents: list):
        """  
        :param sents: лист sents
        :return: отформатированный лист sents, где вместо DocToken стоит Word
        """
        for sent in sents:
            if sent.tokens is None or sent.spans is None:
                ValueError("No tokens or no spans in sent.")
            sent.tokens = self.__word_tokens(sent.tokens)
            sent.spans = self.__word_spans(sent.spans)

    def __add_children(self):
        """  
        добавляет список детей для каждого токена
        """
        children = {token.i: [] for token in self.tokens}

        for token in self.tokens:
            if token.rel != "root":
                children[token.head_i].append(token)

        for i in range(len(self.tokens)):
            self.tokens[i].children = children[i]

    def __add_head(self):
        """  
        добавляет head для каждого токена
        """
        for token in self.tokens:
            token.head = self.tokens[token.head_i]


class Date:
    def __init__(self, match):
        self.start = match.start
        self.stop = match.stop
        self.fact = match.fact
        self.tokens = None
        self.connection = None