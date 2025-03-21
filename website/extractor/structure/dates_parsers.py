from yargy import rule, or_, and_, Parser, predicates
from natasha.grammars.date import Date, DATE

DATE_RULE = DATE

YEAR_PREDICATE = and_(predicates.type("INT"), predicates.length_eq(4))

YEAR_RULE = rule(
    YEAR_PREDICATE.interpretation(Date.year.custom(int))
).interpretation(Date)

CUSTOM_DATE = or_(
    DATE_RULE,
    YEAR_RULE
).interpretation(Date)

all_dates_extractor = Parser(CUSTOM_DATE)

def main():
    text = "2022 - 2023 года и 5 июля 2018"

    matches = all_dates_extractor.findall(text)
    for match in matches:
        print(match)

if __name__ == "__main__":
    main()