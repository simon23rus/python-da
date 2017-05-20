#!/usr/bin/env python3
from collections import defaultdict, OrderedDict, deque
import unittest
import re
import argparse


def tokenize(data):
    return list(re.findall(r'[a-zA-Zа-яА-Я]+|[\d]+|.', data[0]))


def count_probabilities(parsed_arguments, train_text, verbosity=True):
    to_return = []
    depth = parsed_arguments.depth
    probs_for_depths = {}
    for cur_depth in (range(depth + 1)):
        cur_len = defaultdict(float)
        cur_counter = defaultdict(dict)
        for cur_line in range(len(train_text)):
            for cur_pos in range(cur_depth, len(train_text[cur_line])):
                cur_seq = ' '.join(
                    train_text[cur_line][cur_pos - cur_depth: cur_pos])

                if train_text[cur_line][cur_pos] not in cur_counter[cur_seq]:
                    cur_counter[cur_seq][train_text[cur_line][cur_pos]] = 1
                else:
                    cur_counter[cur_seq][train_text[cur_line][cur_pos]] += 1
                cur_len[cur_seq] += 1

        cur_depth_probs = dict()
        for cur_seq in cur_counter:
            cur_depth_probs[cur_seq] = defaultdict(float)
            for next_word in cur_counter[cur_seq]:
                cur_depth_probs[cur_seq][next_word] = \
                    cur_counter[cur_seq][next_word] / cur_len[cur_seq]

        cur_depth_probs = OrderedDict(sorted(cur_depth_probs.items()))
        for cur_seq in cur_depth_probs:
            cur_depth_probs[cur_seq] = OrderedDict(sorted(
                                                   cur_depth_probs[cur_seq]
                                                   .items()))
            probs_for_depths[cur_seq] = cur_depth_probs[cur_seq]

        to_return.append(cur_depth_probs)

    probs_for_depths = OrderedDict(sorted(probs_for_depths.items()))
    if verbosity is True:
        for cur_seq in probs_for_depths:
            print(cur_seq)
            for next_word in probs_for_depths[cur_seq]:
                print('  {}: {:.2f}'.format(
                      next_word, probs_for_depths[cur_seq][next_word]))

    return to_return, probs_for_depths


def generate(parsed_arguments, calculated_probs, verbosity=False):
    depth = parsed_arguments.depth
    size = parsed_arguments.size
    our_text = []
    cur_length = 0
    cur_seq = deque()
    while cur_length < size:
        seq_to_find = cur_seq
        while ' '.join(seq_to_find) not in calculated_probs[len(seq_to_find)]:
            seq_to_find.popleft()
        candidates = calculated_probs[len(seq_to_find)][' '.join(seq_to_find)]
        new_word = max(candidates, key=candidates.get)
        our_text.append(new_word)
        cur_length += 1
        if len(cur_seq) == depth:
            cur_seq.popleft()
        cur_seq.append(new_word)

    return our_text


def main(path='./input.txt', verbosity=True):

    with open(path, 'r') as f:
        data = f.read().splitlines()

    args, data = data[0].split(), data[1:]
    mode, args = args[0], args[1:]
    parser = argparse.ArgumentParser()

    if mode == 'tokenize':
        tokenized_data = tokenize(data)
        print('\n'.join(tokenized_data))

    elif mode == 'probabilities':
        parser.add_argument('--depth', type=int)
        parsed_arguments = parser.parse_args(args)
        tokenized_data = []
        for string in data:
            tokenized_data.append(list(re.findall(r'[\w]+', string)))
        probs, probs_for_depths = count_probabilities(parsed_arguments,
                                                      tokenized_data,
                                                      verbosity)
        return probs, probs_for_depths

    elif mode == 'generate':
        parser.add_argument('--depth', type=int)
        parser.add_argument('--size', type=int)
        parsed_arguments = parser.parse_args(args)
        tokenized_data = []
        for string in data:
            tokenized_data.append(list(re.findall(r'[a-zA-Zа-яА-Я]+|[\d]+|.',
                                  string)))
        calculated_probs, probs_for_depths = count_probabilities(
                                               parsed_arguments,
                                               tokenized_data,
                                               verbosity=False)

        generated = generate(parsed_arguments, calculated_probs)
        if verbosity is True:
            print(''.join(generated))
        return generated

    elif mode == 'test':
        pass
        # because some additional files needed
        # unittest.main()


class TestTokenize(unittest.TestCase):
    def test_1(self):
        answer = ['eto', ' ', 'moi', ' ', 'perviy', ' ', 'test']
        self.assertEqual(tokenize(['eto moi perviy test']), answer)

    def test_2(self):
        answer = ['С', ' ', 'КИРИЛЛИЦЕЙ', '!', ' ', 'РАБОТАЕТ', '!']
        self.assertEqual(tokenize(['С КИРИЛЛИЦЕЙ! РАБОТАЕТ!']), answer)


class TestCountProbabilities(unittest.TestCase):
    def test_1(self):
        _, calculated_probs = main('./pushkin_pamyatnik_depth0.txt', False)
        with open('./ans0pushkin_pamyatnik.txt', 'r') as f:
            answer = f.read().splitlines()

        row_index = 0
        for cur_seq in calculated_probs:
            print(cur_seq)
            for next_word in calculated_probs[cur_seq]:
                ans_word, ans_prob = answer[row_index].split(':')
                ans_prob = float(ans_prob)
                self.assertEqual(next_word, ans_word)
                self.assertEqual(round(
                    calculated_probs[cur_seq][next_word], 2), ans_prob)
                row_index += 1


class TestGenerate(unittest.TestCase):
    def test_1(self):
        generated_text = main('./pushkin_pamyatnik_depth8.txt', False)
        with open('./ans8pushkin_pamyatnik.txt', 'r') as f:
            answer = f.read()
        self.assertEqual(''.join(generated_text), answer)

    def test_2(self):
        generated_text = main('./burns3.txt', False)
        with open('./ans_burns3.txt', 'r') as f:
            answer = f.read()
        self.assertEqual(''.join(generated_text), answer)


if __name__ == '__main__':
    main()
