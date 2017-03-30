from collections import defaultdict


def main():
    n = int(input())

    anagram_groups = defaultdict(list)
    for i in range(n):
        cur_word = input().lower()
        anagram_groups[''.join(sorted(cur_word))].append(cur_word)

    for group in anagram_groups:
        anagram_groups[group] = sorted(set(anagram_groups[group]))

    for elem in sorted(list(anagram_groups.values())):
        if len(elem) <= 1:
            continue
        print(' '.join(elem))


main()
