"""

                 _   _
                | | | | ___  _ __ ___   ___ _ __
                | |_| |/ _ \| '_ ` _ \ / _ \ '__|
                |  _  | (_) | | | | | |  __/ |
                |_| |_|\___/|_| |_| |_|\___|_|


Homer analyzes english text (e.g. a blog post or an essay). Gives reading time, number of total sentences,
readability scores, average sentences per paragraph, average words per sentence, compulsive hedgers, zombie nouns,
and vague words.

Homer can help make your text more clear, simple and useful for the reader.

Author: Waqas Younas
Email: waqas.younas@gmail.com
"""
import operator
import itertools
import nltk
from nltk.corpus import cmudict
from functools import lru_cache
from utils import FleschReading, DaleChall


class Word(object):
    """
    An abstraction of a 'word'. It determines whether a word is a compulsive hedger, an intensifier, an abstract
    noun or a vague word.

    The idea to look for compulsive hedgers, intensifiers and abstract nouns came from Steven Pinker's book
    `The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century`.

    Whereas the idea to look for vague words came after reading both the above book and the following paper:
    https://litlab.stanford.edu/LiteraryLabPamphlet9.pdf
    """

    def __init__(self, word, **kwargs):
        self.syllables = None
        self.word = word.strip().lower()
        self.intensifiers = kwargs.get('intensifiers') or ['very', 'highly', 'extremely']
        self.compulsive_hedgers = kwargs.get('compulsive_hedgers') or ['apparently', 'almost', 'fairly', 'nearly',
                                                                       'partially', 'predominantly', 'presumably', 'rather', 'relative', 'seemingly']
        self.abs_nouns = kwargs.get('abs_nouns') or ["approach", 'assumption', 'concept', 'condition', 'context',
                                                     'framework', 'issue', 'model', 'process', 'range', 'role', 'strategy', 'tendency', 'variable', 'perspective']
        self.vague_words = kwargs.get('vague_words') or ['accrual', 'derivative', 'fair value', 'portfolio', 'audit', 'poverty', 'evaluation',
                                                                'management', 'monitoring', 'effectiveness', 'performance', 'competitiveness',
                                                                'reform', 'assistance', 'growth', 'effort', 'capacity', 'transparency',
                                                                'effectiveness', 'progress', 'stability', 'protection', 'access',
                                                                'implementation', 'sustainable']

    def is_and(self):
            word_and = 'and'
            return self.word == word_and

    def is_compulsive_hedger(self):
        return self.word in self.compulsive_hedgers

    def is_intensifier(self):
        return self.word in self.intensifiers

    def is_vague_word(self):
        # vague word is either an abstract noun or it's in the above list
        return self.word in self.abs_nouns + self.vague_words

    def __repr__(self):
        return self.word

    def __str__(self):
        return self.word



@lru_cache(maxsize=256)
def get_word(word):
    return Word(word)


class Sentence(object):
    """
    An abstraction that represents a sentence. Gives total words, compulsive hedgers, intensifiers,
    abstract nouns, vague words and zombie nouns in a sentence.
    """
    def __init__(self, sentence, **kwargs):
        self.sentence = sentence
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word.isalpha() or word.isdigit()]
        self._words = [get_word(word) for word in words]
        # zombies are verbs or adjectives that end with following
        self.zombies = kwargs.get('zombies') or ['ance', 'ment', 'ments', 'tion', 'tions', 'ism', 'ity']

    @property
    def words(self):
        return self._words

    @property
    def total_words(self):
        return len(self.words)

    @property
    def total_and_words(self):
        return len([word for word in self.words if word.is_and()])

    def get_compulsive_hedgers(self):
        return (word for word in self.words if word.is_compulsive_hedger())

    def get_intensifiers(self):
        return (word for word in self.words if word.is_intensifier())

    def get_vague_words(self):
        return (word for word in self.words if word.is_vague_word())

    def get_zombie_nouns(self):
        words = nltk.word_tokenize(self.sentence)
        tags = nltk.pos_tag(words)
        zombie_nouns = []
        for word, tag in tags:
            if tag.startswith('VB') or tag.startswith('JJ'):
                if any(word.endswith(zombie) for zombie in self.zombies):
                    zombie_nouns.append(word)
        return zombie_nouns

    def __str__(self):
        return self.sentence


class Paragraph(object):
    """
    Represents a paragraph. Gives compulsive hedgers, intensifiers, abstract nouns,
    zombie nouns, vague words, and readability scores of a paragraph. Moreover, it gives us total words,
    total sentences, longest sentence and avg words per sentence in a paragraph.
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
    def total_sentences(self):
        return len(self.sentences)

    @property
    def total_words(self):
        return sum([sentence.total_words for sentence in self.sentences])

    @property
    def total_and_words(self):
        return sum([sentence.total_and_words for sentence in self.sentences if sentence.total_and_words])

    @property
    def avg_words_per_sentence(self):
        return round(self.total_words / self.total_sentences, 2)

    @property
    def longest_sentence(self):
        return max(self.tokenized_sentences)

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

    def get_zombie_nouns(self):
        return list(itertools.chain(*[sentence.get_zombie_nouns() for sentence in self.sentences
                                                   if sentence.get_zombie_nouns()]))

    def get_vague_words(self):
        return list(itertools.chain(*[sentence.get_vague_words() for sentence in self.sentences
                                                  if sentence.get_vague_words()]))

    def __repr__(self):
        return "sentences= {sentences}, flesch_reading_score={flesch_reading}, dale_chall={dale_chall}".format(
            sentences=self.total_sentences, flesch_reading=self.get_flesch_reading_score(),
            dale_chall=self.get_dale_chall_reading_score())


class Article(object):
    """
    This represents a block of text, i.e. an essay, a blog or an article.

    Using this, we can retrieve article-level as well as paragraph-level stats.
    """
    def __init__(self, name, author, text):
        self.name = name
        self.author = author
        # Replacing em dash and en dash
        text = text.replace('—', ' ')
        self.text = text
        paragraphs = nltk.tokenize.blankline_tokenize(text)
        self._paragraphs = [Paragraph(paragraph) for paragraph in paragraphs]

    @property
    def paragraphs(self):
        return self._paragraphs

    @property
    def total_sentences(self):
        return sum([paragraph.total_sentences for paragraph in self.paragraphs])

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
        words_one_reads_per_minute = 200
        return self.total_words / words_one_reads_per_minute

    @property
    def avg_sentences_per_para(self):
        return round(self.total_sentences / self.total_paragraphs, 2)

    @property
    def avg_words_per_sentence(self):
        return round(self.total_words / self.total_sentences, 2)

    def get_paragraphs(self):
        return self.paragraphs

    def get_flesch_reading_score(self):
        return FleschReading(self.text).grade()

    def get_dale_chall_reading_score(self):
        return DaleChall(self.text).grade()

    def get_intensifiers(self):
        return list(itertools.chain(*(paragraph.get_intensifiers() for paragraph in self.paragraphs
                                                   if paragraph.get_intensifiers())))

    def get_vague_words(self):
        return list(itertools.chain(*(paragraph.get_vague_words() for paragraph in self.paragraphs
                                                  if paragraph.get_vague_words())))

    def get_compulsive_hedgers(self):
        return list(itertools.chain(*(paragraph.get_compulsive_hedgers() for paragraph in self.paragraphs
                                                         if paragraph.get_compulsive_hedgers())))

    def get_zombie_nouns(self):
        return list(itertools.chain(*(paragraph.get_zombie_nouns() for paragraph in self.paragraphs
                                                   if paragraph.get_zombie_nouns())))

    def get_and_frequency(self):
        return str(round(self.total_and_words / self.total_words * 100, 2)) + " %"

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
