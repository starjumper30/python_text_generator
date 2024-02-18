import random

from nltk import regexp_tokenize, bigrams, trigrams

SENTENCE_ENDERS = '!.?'


class BiGram:

    def __init__(self, head):
        self.head = head
        self.tails = {}

    def print_tails(self):
        for tail, count in self.tails.items():
            print(f'Tail: {tail:10}\t Count: {count}')

    def add_tail(self, tail):
        count = self.tails.get(tail, 0)
        self.tails[tail] = count + 1

    def random_tail(self):
        return random.choices(list(self.tails.keys()), list(self.tails.values()))[0]

    def is_first_word_eligible(self):
        true_head = self.head.split(' ')[0]
        return true_head[0].istitle() and true_head[-1] not in SENTENCE_ENDERS


def parse_file(file_name):
    with open(file_name, 'rt', encoding='utf-8') as fh:
        words = [word for line in fh for word in regexp_tokenize(line, '\\S+')]

    bigrams_dict = {}
    for first, middle, tail in trigrams(words):
        head = f'{first} {middle}'
        bigram = bigrams_dict.get(head, BiGram(head))
        bigram.add_tail(tail)
        bigrams_dict[head] = bigram
    return bigrams_dict


def main():
    file_name = input()
    bigrams_dict = parse_file(file_name)
    first_words = [bigram.head for bigram in bigrams_dict.values() if bigram.is_first_word_eligible()]
    for _ in range(10):
        head = random.choices(first_words)[0]
        words = [word for word in head.split(' ')]
        while len(words) < 5 or words[-1][-1] not in SENTENCE_ENDERS:
            tail = bigrams_dict.get(head).random_tail()
            head = f'{words[-1]} {tail}'
            words.append(tail)
        print(*words, sep=' ')


if __name__ == '__main__':
    main()
