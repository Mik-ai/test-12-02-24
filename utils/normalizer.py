import re
from dateparser import parse


def convert_date(date_str) -> str:
    try:
        return parse(date_str, languages=["ru"]).strftime("%d.%m.%Y")
    except Exception:
        return date_str


def preprocess_date_word(match_unit: str):
    x = ["год", "месяц", "ден", "недел"]
    for i in x:
        if i in match_unit:
            return i
    return match_unit


def convert_duration(phrase):
    pattern = r"(?:в течение)?\s*(?:([\d,\.]+)\s*(?:года|лет|месяцев|месяц|недели|недель|дней|дня|день))"
    occurrences = re.finditer(pattern, phrase, re.IGNORECASE)

    years, months, weeks, days = 0, 0, 0, 0

    for ocur in occurrences:
        string = ocur.group().strip()
        match_int = int(re.sub(r"\D", "", string))
        match_unit = preprocess_date_word(re.sub(r"\d", "", string).strip())

        match match_unit:
            case "лет" | "год":
                years = match_int
            case "месяц":
                months = match_int
            case "недел":
                weeks = match_int
            case "ден" | "дня" | "дней":
                days = match_int

    return f"{years}_{months}_{weeks}_{days}"


converters = {
    "ДатаДокумента": convert_date,
    "СрокОплаты": convert_duration,
}


def normalize(tree) -> str:
    if isinstance(tree, dict):
        for key, value in tree.items():
            if key not in converters:
                tree[key] = normalize(value)
            else:
                tree[key] = converters[key](value)
        return tree
    elif isinstance(tree, list):
        return [normalize(item) for item in tree]
    else:
        return tree
