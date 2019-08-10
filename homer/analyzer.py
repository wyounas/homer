"""

                 _   _
                | | | | ___  _ __ ___   ___ _ __
                | |_| |/ _ \| '_ ` _ \ / _ \ '__|
                |  _  | (_) | | | | | |  __/ |
                |_| |_|\___/|_| |_| |_|\___|_|


Homer can help make your text more clear, simple and useful for the reader.

Homer analyzes english text (e.g. a blog post or an essay). Gives reading time, readability scores, paragraph and
sentence level stats.

Author: Waqas Younas
Email: waqas.younas@gmail.com
"""
import operator
import itertools
import nltk
from nltk.corpus import cmudict
from functools import lru_cache
from homer.utils import FleschReading, DaleChall
from homer.constants import INTENSIFIERS, COMPULSIVE_HEDGERS, VAGUE_WORDS, MAX_WORDS_IN_SENTENCE,\
    MAX_SENTENCES_IN_PARAGRAPH, WORDS_ONE_READS_PER_MINUTE


class Word(object):
    """
    An abstraction of a 'word'. It determines whether a word is a compulsive hedger, an intensifier or a vague word.

    The idea to look for compulsive hedgers, intensifiers and vague words came from the following works:
    - Steven Pinker's book `The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century`.
    - https://litlab.stanford.edu/LiteraryLabPamphlet9.pdf
    """

    def __init__(self, word, intensifiers=INTENSIFIERS, compulsive_hedgers=COMPULSIVE_HEDGERS,
                 vague_words=VAGUE_WORDS):
        self.syllables = None
        self.word = word.strip().lower()
        self.intensifiers = intensifiers
        self.compulsive_hedgers = compulsive_hedgers
        self.vague_words = vague_words

    def is_and(self):
            word_and = 'and'
            return self.word == word_and

    def is_compulsive_hedger(self):
        return self.word in self.compulsive_hedgers

    def is_intensifier(self):
        return self.word in self.intensifiers

    def is_vague_word(self):
        return self.word in self.vague_words

    def __repr__(self):
        return 'Word(%r)' % self.word

    def __str__(self):
        return self.word


@lru_cache(maxsize=256)
def get_word(word):
    return Word(word)


class Sentence(object):
    """
    An abstraction that represents a sentence and gives various stats.
    """
    def __init__(self, sentence):
        self.sentence = sentence
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word.isalpha() or word.isdigit()]
        self._words = [get_word(word) for word in words]

    @property
    def words(self):
        return self._words

    @property
    def total_and_words(self):
        return len([word for word in self.words if word.is_and()])

    def is_long(self):
        return len(self) > MAX_WORDS_IN_SENTENCE

    def get_compulsive_hedgers(self):
        return (word for word in self.words if word.is_compulsive_hedger())

    def get_intensifiers(self):
        return (word for word in self.words if word.is_intensifier())

    def get_vague_words(self):
        return (word for word in self.words if word.is_vague_word())

    def __len__(self):
        return len(self.words)

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __repr__(self):
        return 'Sentence(%r)' % self.sentence

    def __str__(self):
        return self.sentence


class Paragraph(object):
    """
    Represents a paragraph. Finds compulsive hedgers, intensifiers, vague words, readability scores of a paragraph and
    various other stats.
    """

    def __init__(self, paragraph):
        paragraph = paragraph.replace('—', ' ')
        self.paragraph = paragraph
        self.tokenized_sentences = nltk.sent_tokenize(paragraph)
        self._sentences = [Sentence(sentence) for sentence in self.tokenized_sentences]


    @property
    def sentences(self):
        return self._sentences

    @property
    def longest_sentence(self):
        return max(self._sentences, key=lambda sentence: len(sentence))

    @property
    def total_words(self):
        return sum([len(sentence) for sentence in self.sentences])

    @property
    def total_and_words(self):
        return sum([sentence.total_and_words for sentence in self.sentences if sentence.total_and_words])

    @property
    def avg_words_per_sentence(self):
        round_to_two_digits = 2
        return round(self.total_words / len(self), round_to_two_digits)

    def is_long(self):
        return len(self) >= MAX_SENTENCES_IN_PARAGRAPH

    def get_flesch_reading_score(self):
        return FleschReading(self.paragraph).grade()

    def get_dale_chall_reading_score(self):
        return DaleChall(self.paragraph).grade()

    def get_intensifiers(self):
        return list(itertools.chain(*[sentence.get_intensifiers() for sentence in self.sentences
                                                   if sentence.get_intensifiers()]))

    def get_compulsive_hedgers(self):
        return list(itertools.chain(*[sentence.get_compulsive_hedgers() for sentence in self.sentences
                                                         if sentence.get_compulsive_hedgers()]))

    def get_vague_words(self):
        return list(itertools.chain(*[sentence.get_vague_words() for sentence in self.sentences
                                                  if sentence.get_vague_words()]))

    def __len__(self):
        return len(self.sentences)

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __repr__(self):
        return 'Paragraph(%r)' % self.paragraph


class Article(object):
    """
    This represents a block of text, i.e. an essay, a blog or an article.

    Using this, we can retrieve article as well as paragraph-level stats.
    """
    def __init__(self, name, author, text):
        self.name = name
        self.author = author
        # Replacing em dash and en dash
        self.text = text.replace('—', ' ')
        paragraphs = nltk.tokenize.blankline_tokenize(text)
        self._paragraphs = [Paragraph(paragraph) for paragraph in paragraphs]

    @property
    def paragraphs(self):
        return self._paragraphs

    @property
    def len_of_longest_paragraph(self):
        return len(max(self._paragraphs, key=lambda paragraph: len(paragraph)))

    @property
    def longest_sentence(self):
        return max([paragraph.longest_sentence for paragraph in self._paragraphs], key=lambda sentence: len(sentence))

    @property
    def len_of_longest_sentence(self):
        return len(self.longest_sentence)

    @property
    def total_sentences(self):
        return sum([len(paragraph) for paragraph in self.paragraphs])

    @property
    def total_paragraphs(self):
        return len(self.paragraphs)

    @property
    def total_words(self):
        return sum([paragraph.total_words for paragraph in self.paragraphs])

    @property
    def total_and_words(self):
        return sum([paragraph.total_and_words for paragraph in self.paragraphs])

    @property
    def reading_time(self):
        return self.total_words / WORDS_ONE_READS_PER_MINUTE

    @property
    def avg_sentences_per_para(self):
        round_to_two_digits = 2
        return round(self.total_sentences / self.total_paragraphs, round_to_two_digits)

    @property
    def avg_words_per_sentence(self):
        round_to_two_digits = 2
        return round(self.total_words / self.total_sentences, round_to_two_digits)

    def get_paragraphs(self):
        return self.paragraphs

    def get_flesch_reading_score(self):
        return FleschReading(self.text).grade()

    def get_dale_chall_reading_score(self):
        return DaleChall(self.text).grade()

    def is_difficult_to_read(self):
        return FleschReading(self.text).is_difficult()

    def get_intensifiers(self):
        return list(itertools.chain(*(paragraph.get_intensifiers() for paragraph in self.paragraphs
                                                   if paragraph.get_intensifiers())))

    def get_vague_words(self):
        return list(itertools.chain(*(paragraph.get_vague_words() for paragraph in self.paragraphs
                                                  if paragraph.get_vague_words())))

    def get_compulsive_hedgers(self):
        return list(itertools.chain(*(paragraph.get_compulsive_hedgers() for paragraph in self.paragraphs
                                                         if paragraph.get_compulsive_hedgers())))

    def get_and_frequency(self):
        round_to_two_digits = 2
        return str(round(self.total_and_words / self.total_words * 100, round_to_two_digits)) + " %"

    def ten_words_with_most_syllables(self):
        """This gets us 10 words with most syllables in a text"""
        d = cmudict.dict()
        words = nltk.word_tokenize(self.text)
        syllable_data = {}
        for word in words:
            word = word.strip().lower()
            if word not in syllable_data:
                try:
                    syllable_data[word] = [len(list(y for y in x if y[-1].isdigit())) for x in d[word]][0]
                except KeyError:
                    pass  # Perhaps this word is not in the cmudict
        return [item[0] for item in list(reversed(sorted(syllable_data.items(), key=operator.itemgetter(1))))[:10]]

    def get_n_most_repeated_words(self, n):
        """Gets us n most repeated words in the text. """
        words = nltk.word_tokenize(self.text)
        stopwords = nltk.corpus.stopwords.words('english')
        all_words_except_stop = nltk.FreqDist(w.lower() for w in words if w[0].isalpha() and w not in stopwords)
        return [word for word, freq in all_words_except_stop.most_common(n)]
