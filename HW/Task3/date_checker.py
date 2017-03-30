import re


def main():
    with open('input.txt', 'r') as f:
        data = f.read().splitlines()

    for date in data:
        match = re.match(
            r'\d\d(\.|-|\/)\d\d\1\d\d\d\d|'
            + r'\d\d\d\d(\.|-|\/)\d\d\2\d\d|\d{1,2}\ *[а-яА-Я]+\ *\d\d\d\d',
            date)
        if match and match.start() == 0 and match.end() == len(date):
            print("YES")
        else:
            print("NO")


main()
