import re
import json
from string import punctuation as punct


def find_nes(logs, dicts):
    found_nes = []
    counter = 0
    for log in logs:
        matches = []
        ne_found = False
        for ne_type in dicts:
            for ne in dicts[ne_type]:
                if ne != 'Игра':
                    ne_orig_reg = r' '.join(fr'\b{word}\b' for word in ne.strip(punct).split())
                    reg = fr'(({dicts[ne_type][ne]})|({ne_orig_reg}))'
                    try:
                        match = re.search(reg, log, flags=re.I)
                    except re.error:
                        match = re.search(dicts[ne_type][ne], log, flags=re.I)
                    if match:
                        match_type = re.sub(r'\d', '', ne_type)
                        match_span = match.span()
                        matches.append((ne, range(match_span[0], match_span[1] + 1), match_type))
                        if not ne_found:
                            ne_found = True
                            counter += 1
        if ne_found:
            wrong_matches = []
            for match in matches:
                for another_match in matches:
                    match_set = set(match[1])
                    if match_set.intersection(another_match[1]):
                        if len(match[1]) > len(another_match[1]):
                            wrong_matches.append(another_match)
                        elif len(another_match[1]) > len(match[1]):
                            wrong_matches.append(match)
            true_matches = list(set(matches) - set(wrong_matches))
            nes = []
            for match in true_matches:
                nes.append({'ne': match[0], 'span': (match[1][0], match[1][-1]), 'type': match[2]})
            found_nes.append({'log': log, 'nes': nes})
    print(f'ИС найдены в {counter} логах из {len(logs)}')
    return found_nes


def main():
    with open('dicts_with_regex.json', 'r', encoding='utf-8') as f:
        dicts_with_regex = json.load(f)

    with open('log.txt', encoding='utf-8') as f:
        logs = f.read()

    logs = logs.split('\n')

    found_nes = find_nes(logs, dicts_with_regex)

    with open('found_nes.json', 'w', encoding='utf-8') as fw:
        json.dump(found_nes, fw, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
