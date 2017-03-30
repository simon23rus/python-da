def main():
    n = int(input())
    import re
    for ind in range(n):
        row = input()
        new_row = (re.sub('\W', '', row.lower()))
        new_row = new_row.replace('ё', 'е')
        is_palindrom = True
        for j in range(len(new_row) // 2):
            if new_row[j] != new_row[-(j + 1)]:
                print('no')
                is_palindrom = False
                break

        if is_palindrom:
            print('yes')


main()
