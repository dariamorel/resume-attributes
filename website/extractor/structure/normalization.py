from datetime import datetime
from natasha import Doc, Segmenter

segmenter = Segmenter()

def normalize_sent(sent, lower=False):
    """
    Функция очищает предложение от лишних символов в начале и в конце, а также переводит первую букву в верхний регистр.
    :param sent: исходное предложение
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
    :param text: исходный текст
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

def name_to_str(fact):
    """
    Функция преобразует ФИО из формата fact в формат str.
    """
    result = ""
    if fact.last:
        last = fact.last[0].upper() + fact.last[1:].lower()
        result += f"{last} "
    if fact.first:
        first = fact.first[0].upper() + fact.first[1:].lower()
        result += f"{first} "
    if fact.middle:
        middle = fact.middle[0].upper() + fact.middle[1:].lower()
        result += f"{middle} "
    return result.strip()

def date_to_str(fact):
    """
    Функция преобразует дату из формата fact в формат str.
    """
    if fact.year == "now":
        return "настоящее время"
    months = {
        1: "январь", 2: "февраль", 3: "март", 4: "апрель",
        5: "май", 6: "июнь", 7: "июль", 8: "август",
        9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
    }

    if fact.day and fact.month and fact.year:
        formated_date = datetime(year=fact.year, month=fact.month, day=fact.day)
        return formated_date.strftime("%d %B %Y года")
    elif fact.month and fact.year:
        return f"{months[fact.month]} {fact.year} года"
    elif fact.year:
        formated_date = datetime(year=fact.year, month=1, day=1)
        return formated_date.strftime("%Y год")

def lemmatize_phone_number(number):
    """
    Функция приводит номер телефона к единному формату.
    """
    digits = ""
    for char in number:
        if char.isdigit() and len(digits) == 0 and char == '8':
            digits += '7'
        elif char.isdigit():
            digits += char
    if len(digits) != 11:
        return number

    return f"+{digits[0]} ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"