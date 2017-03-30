import re


def cleaner(strink):
    if strink.split()[0] == 'import':
        modules = re.split(r', ', strink)
        modules[0] = modules[0].split()[-1]
    #     print(modules)
        return modules
    else:
        pos = strink.find(' import ')
        strink = strink[:pos]
        modules = re.split(r', ', strink)
        modules[0] = modules[0].split()[-1]
        return modules


def main():
    with open('input.txt') as f:
        text = f.read()
    imports = []
    for match in re.finditer(
        r'(import [\w\.|\w\, ]+)|(from [\w\.]+ import [\w\.]+)',
            text):
        imports.append(text[match.start(): match.end()])

    ans = []
    for lis in list(map(cleaner, imports)):
        ans += lis

    print(', '.join(sorted(set(ans))))


main()
