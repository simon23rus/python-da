from collections import defaultdict


def main():
    with open('input.txt', 'r') as f:
        data = f.read().splitlines()

    delimeter_pos = 0
    while(data[delimeter_pos] != ''):
        delimeter_pos += 1
    lang_info = data[:delimeter_pos]
    texts = data[delimeter_pos + 1:]

    symbol_to_lang = {}
    for lang_in in lang_info:
        lang, letters = lang_in.split()
        for letter in letters:
            symbol_to_lang[letter] = lang

    for text in texts:
        text_langs = set()
        for word in text.lower().split():
            lang_letters = defaultdict(int)
            for symbol in word:
                if symbol in symbol_to_lang:
                    lang_letters[symbol_to_lang[symbol]] -= 1
            if len(lang_letters) == 0:
                continue
            else:
                text_langs.add(min(list(lang_letters.items()),
                               key=lambda x: (x[1], x[0]))[0])
        if len(text_langs) == 0:
            print('')
        else:
            print(' '.join(sorted(text_langs)))


main()
