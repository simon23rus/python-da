#!/usr/bin/env python3
from collections import defaultdict, OrderedDict, deque
import unittest
import re
import argparse


def tokenize(data, verbosity=True):
    result = (list(re.findall(r'[a-zA-Zа-яА-Я]+|[\d]+|.', data[0])))
    if verbosity is True:
        print('\n'.join(result))
    return result


def count_probabilities(parsed, cur_data, verbosity=True):
    to_return = []
    depth = parsed.depth
    giant_dict = {}
    for cur_depth in (range(depth + 1)):
        cur_len = defaultdict(float)
        cur_counter = defaultdict(dict)
        for i in range(len(cur_data)):
            for j in range(cur_depth, len(cur_data[i])):
                cur_seq = ' '.join(cur_data[i][j - cur_depth: j])
                if cur_data[i][j] not in cur_counter[cur_seq]:
                    cur_counter[cur_seq][cur_data[i][j]] = 1
                else:
                    cur_counter[cur_seq][cur_data[i][j]] += 1
                cur_len[cur_seq] += 1
        ansa = dict()
        for k in cur_counter:
            ansa[k] = defaultdict(float)
            for k2 in cur_counter[k]:
                ansa[k][k2] = cur_counter[k][k2] / cur_len[k]

        ansa = OrderedDict(sorted(ansa.items()))
        for k in ansa:
            ansa[k] = OrderedDict(sorted(ansa[k].items()))
            giant_dict[k] = ansa[k]
#             for val in ansa[k]:
#                 print('  {}: {:.2f}'.format(val, ansa[k][val]))

        to_return.append(ansa)
    giant_dict = OrderedDict(sorted(giant_dict.items()))
    if verbosity is True:
        for k in giant_dict:
            print(k)
    #         ansa[k] = OrderedDict(sorted(ansa[k].items()))
    #         giant_dict[k] = ansa[k]
            for val in giant_dict[k]:
                print('  {}: {:.2f}'.format(val, giant_dict[k][val]))

    return to_return


def generate(parsed, cur_data, verbosity=False):
    depth = parsed.depth
    size = parsed.size
    calculated_probs = count_probabilities(parsed, cur_data,
                                           verbosity=verbosity)
    our_text = []
    cur_lenght = 0
    cur_seq = deque()
    while(cur_lenght < size):
        seq_to_find = cur_seq
        while ' '.join(seq_to_find) not in calculated_probs[len(seq_to_find)]:
            seq_to_find.popleft()
        candidates = calculated_probs[len(seq_to_find)][' '.join(seq_to_find)]
        new_word = max(candidates, key=candidates.get)
        our_text.append(new_word)
        cur_lenght += 1
        if len(cur_seq) == depth:
            cur_seq.popleft()
        cur_seq.append(new_word)

    return our_text


def main():

    with open('./input.txt', 'r') as f:
        data = f.read().splitlines()

    args, data = data[0].split(), data[1:]
    mode, args = args[0], args[1:]

    parser = argparse.ArgumentParser()

    if mode == 'tokenize':
        tokenize(data)

    elif mode == 'probabilities':
        parser.add_argument('--depth', type=int)
        parsed = parser.parse_args(args)
        tokenized_data = []
        for string in data:
            tokenized_data.append(list(re.findall(r'[\w]+', string)))
        probs = count_probabilities(parsed, tokenized_data)
        return probs

    elif mode == 'generate':
        parser.add_argument('--depth', type=int)
        parser.add_argument('--size', type=int)
        parsed = parser.parse_args(args)
        tokenized_data = []
        for string in data:
            tokenized_data.append(list(re.findall(r'[a-zA-Zа-яА-Я]+|[\d]+|.',
                                  string)))
        generated = generate(parsed, tokenized_data)
        print(''.join(generated))
        return generated

    elif mode == 'test':
        unittest.main()


class TestTokenize(unittest.TestCase):
    def test_1(self):
        answer = ['eto', ' ', 'moi', ' ', 'perviy', ' ', 'test']
        self.assertEqual(tokenize(['eto moi perviy test']), answer)

    def test_2(self):
        answer = ['С', ' ', 'КИРИЛЛИЦЕЙ', '!', ' ', 'РАБОТАЕТ', '!']
        self.assertEqual(tokenize(['С КИРИЛЛИЦЕЙ! РАБОТАЕТ!']), answer)


if __name__ == '__main__':
    main()
