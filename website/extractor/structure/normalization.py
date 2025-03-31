from natasha import Doc, Segmenter
segmenter = Segmenter()

def normalize_sent(sent, lower=False):
    """
    Функция очищает предложение от лишних символов в начале и в конце, а также переводит первую букву в верхний регистр.
    :param sent: изначальное предложение
    :param lower: флаг, отвечающий за то, нужно ли переводить остальную часть предложения в нижний регистр
    :return: отформатированное предложение
    """
    sent = sent.strip()
    if len(sent) == 0:
        return None
    # Убираем спец символы в начале и в конце
    while not (sent[0].isalpha() or sent[0].isdigit()):
        if sent[0] == '+':
            break
        sent = sent[1:]
        if len(sent) == 0:
            return None
    while not (sent[-1].isalpha() or sent[-1].isdigit()):
        if sent[-1] in [')', ']', '}', '"', "'", "+"]:
            break
        sent = sent[:-1]
        if len(sent) == 0:
            return None

    if lower:
        sent = sent.lower()
    # Проверяем, чтобы первая буква была заглавной
    return sent[0].upper() + sent[1:]

def delete_additional_info(text):
    """
    Функция убирает дополнительную информацию в круглых скобках, которая не несет основного смысла.
    :param text: изначальный текст
    :return: отформатированный текст
    """
    doc = Doc(text)
    doc.segment(segmenter)
    start, stop = 0, len(text)
    normalized_text = ""
    for token in doc.tokens:
        if token.text == '(':
            stop = token.start
            normalized_text += text[start:stop]
        if token.text == ')':
            start = token.stop
    normalized_text += text[start:]
    return normalized_text