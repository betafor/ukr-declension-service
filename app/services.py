import pymorphy3
import pymorphy3_dicts_uk
import re

morph = pymorphy3.MorphAnalyzer(path=pymorphy3_dicts_uk.get_path(), lang='uk')


def decline_fio_word(word: str, word_type: str, gender: str, target_case: str) -> str:

    if word is None or not str(word).strip():
        return ""

    # ЗАХИСТ: Українські прізвища (тип 'ln') НЕ відмінюються в кличний відмінок (voct)
    if word_type == 'ln' and target_case == 'voct':
            return word.capitalize()

    parsed = morph.parse(word)
    if not parsed:
        return word

    gender_tag = 'masc' if gender == "M" else 'femn'
    best_match = None

    for p in parsed:
        if word_type == 'ln' and 'Surn' in p.tag:
            if gender == "F" and not word.endswith(('а', 'я', 'і', 'ова', 'ая')):
                return word
            best_match = p
            break
        elif word_type == 'fn' and 'Name' in p.tag and gender_tag in p.tag:
            best_match = p
            break
        elif word_type == 'mn' and 'Patr' in p.tag and gender_tag in p.tag:
            best_match = p
            break

    # Если точного совпадения по ФИО-тегам нет, берем самый первый базовый разбор слова
    if not best_match:
        best_match = parsed[0]

    try:
        declined = best_match.inflect({target_case})
        return declined.word.capitalize() if declined else word
    except Exception:
        return word


def decline_phrase_smart(phrase: str, target_case: str) -> str:
    words = phrase.split()
    declined_words = []
    stop_declension = False

    for word in words:
        clean_word = word.strip(",.()\"")
        if not clean_word:
            declined_words.append(word)
            continue

        # ЗАЩИТА 1: Аббревиатуры на капсе (ТОВ, ЦФО, КДП) или чистая латиница (IT, HR)
        # Возвращаем как есть, но НЕ останавливаем склонение фразы (флаг не взводим)
        if clean_word.isupper() or re.match(r'^[a-zA-Z]+$', clean_word):
            declined_words.append(word)
            continue

        # ЗАЩИТА 2: Гибриды через дефис с латиницей или капсом (IT-департамент, PR-відділ)
        if '-' in clean_word:
            parts = clean_word.split('-')
            # Если первая часть — латиница или капс, а вторая — украинское слово
            if (re.match(r'^[a-zA-Z]+$', parts[0]) or parts[0].isupper()) and parts[1]:
                parsed_part = morph.parse(parts[1])
                if parsed_part:
                    p = parsed_part[0]
                    # Проверяем украинские стоп-теги для второй части
                    if 'PREP' in p.tag or 'CONJ' in p.tag or stop_declension:
                        declined_words.append(word)
                        continue
                    if 'gent' in p.tag or 'datv' in p.tag or 'ablt' in p.tag:
                        stop_declension = True
                        declined_words.append(word)
                        continue

                    try:
                        declined_part = p.inflect({target_case})
                        if declined_part:
                            # Собираем обратно с сохранением регистра: IT-департаменту
                            new_word = f"{parts[0]}-{declined_part.word}"
                            final_word = word.replace(clean_word, new_word)
                            declined_words.append(final_word)
                            continue
                    except Exception:
                        declined_words.append(word)  # Зберігаємо оригінал
                        continue  # Йдемо до наступного слова
        # БАЗОВАЯ ЛОГИКА
        parsed_list = morph.parse(clean_word)
        if not parsed_list:
            declined_words.append(word)
            continue
        parsed = parsed_list[0]

        if 'PREP' in parsed.tag or 'CONJ' in parsed.tag:
            stop_declension = True

        if stop_declension:
            declined_words.append(word)
            continue

        if 'gent' in parsed.tag or 'datv' in parsed.tag or 'ablt' in parsed.tag:
            stop_declension = True
            declined_words.append(word)
            continue

        try:
            declined = parsed.inflect({target_case})
            if declined:
                new_word = declined.word
                if clean_word.istitle():
                    new_word = new_word.capitalize()
                final_word = word.replace(clean_word, new_word)
                declined_words.append(final_word)
            else:
                declined_words.append(word)
        except Exception:
            declined_words.append(word)

    return " ".join(declined_words)
