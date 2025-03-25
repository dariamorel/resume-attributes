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