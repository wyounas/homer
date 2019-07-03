"""

                 _   _
                | | | | ___  _ __ ___   ___ _ __
                | |_| |/ _ \| '_ ` _ \ / _ \ '__|
                |  _  | (_) | | | | | |  __/ |
                |_| |_|\___/|_| |_| |_|\___|_|


Contains a class that can help run an analysis on a text (e.g. a blog post or an essay). You can get reading time,
number of total sentences, readability scores (e.g. Flesch reading ease, Dale Chall readability scores), avg
sentences per para, avg words per sentence, compulsive hedgers, zombie nouns, and vague words.

Using this data you can make your text more clear, simple and useful for the reader.

Main class to use is ```Article```. Create its instance and call its methods to see results.

Author: Waqas Younas
Email: waqas.younas@gmail.com
Website: https://blog.wyounas.com
"""
import operator
import itertools
import textstat
import nltk
from colorclass import Color
from terminaltables import SingleTable
from nltk.corpus import cmudict
from functools import lru_cache


class FleschReading(object):
    """https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_reading_ease"""

    def __init__(self, text):
        self.score = textstat.flesch_reading_ease(text)

    def grade(self):
        if 0 <= self.score < 30:
            return 'Very difficult'
        elif 30 <= self.score < 50:
            return 'Difficult'
        elif 50 <= self.score < 60:
            return 'Fairly difficult'
        elif 60 <= self.score < 70:
            return 'Plain English'
        elif 70 <= self.score < 80:
            return 'Fairly easy'
        elif 80 <= self.score < 90:
            return 'Easy'
        elif 90 <= self.score <= 100:
            return 'Very easy'


class DaleChall(object):
    """https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula"""

    def __init__(self, text):
        self.score = round(textstat.dale_chall_readability_score(text), 1)

    def grade(self):
        if self.score <= 4.9:
            return 'Average 4th grade student or lower'
        elif 5.0 <= self.score <= 5.9:
            return 'Average 5th or 6th grade student'
        elif 6.0 <= self.score <= 6.9:
            return 'Average 7th or 8th grade student'
        elif 7.0 <= self.score <= 7.9:
            return 'Average 9th or 10th grade student'
        elif 8.0 <= self.score <= 8.9:
            return 'Average 11th or 12th grade student'
        elif self.score >= 9.0:
            return 'Average 13th or 15th grade student'


class Word(object):
    """An abstraction of a 'word'. It categorizes whether a word is a compulsive hedger, an intensifier, abstract
    noun or a vague word.
    The idea to look for compulsive hedgers, intensifiers and abstract nouns came from Steven Pinker's book
    `The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century`.

    Whereas the idea to look for vague words came after reading this paper:
    https://litlab.stanford.edu/LiteraryLabPamphlet9.pdf
    """

    def __init__(self, word):
        self.syllables = None
        self.word = word.strip().lower()
        self.is_and = True if self.word == 'and' else False
        # Is it a compulsive hedger?
        compulsive_hedgers = ['apparently', 'almost', 'fairly', 'nearly', 'partially', 'predominantly', 'presumably',
                              'rather', 'relative', 'seemingly']
        self.is_compulsive_hedger = True if self.word in compulsive_hedgers else False
        # Is it an intensifier?
        intensifiers = ['very', 'highly', 'extremely']
        self.is_intensifier = True if self.word in intensifiers else False
        # Is it an abstract noun
        abs_nouns = ["approach", 'assumption', 'concept', 'condition', 'context', 'framework', 'issue', 'model',
                     'process', 'range', 'role', 'strategy', 'tendency', 'variable', 'perspective']
        # Check if this word is a zombie noun
        zombies = ['ance', 'ment', 'ments', 'ation', 'ations', 'ing', 'ty']
        # 'vague_words' is a combination of vague words and abstract nouns
        vague_words = ['accrual', 'derivative', 'fair value', 'portfolio', 'audit', 'poverty', 'evaluation',
                       'management', 'monitoring', 'effectiveness', 'performance', 'competitiveness',
                       'reform', 'assistance', 'growth', 'effort', 'capacity', 'transparency',
                       'effectiveness', 'progress', 'stability', 'protection', 'access',
                       'implementation', 'sustainable'] + abs_nouns

        self.is_vague = True if self.word in vague_words else False

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word



@lru_cache(maxsize=256)
def get_word(word):
    return Word(word)


class Sentence(object):
    """An abstraction that represents a sentence. We keep track of compulsive hedgers, intensifiers, abstract nouns,
    vague words and zombie nouns in a sentence. """
    def __init__(self, sentence):
        self.sentence = sentence
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word.isalpha() or word.isdigit()]
        self.words = [get_word(word) for word in words]
        self.compulsive_hedgers = (word for word in self.words if word.is_compulsive_hedger)
        self.intensifiers = (word for word in self.words if word.is_intensifier)
        self.vague_words = (word for word in self.words if word.is_vague)
        self.zombie_nouns = self.get_zombie_nouns()
        self.total_words = len(self.words)
        self.total_and_words = len([word for word in self.words if word.is_and])

    def __str__(self):
        return self.sentence

    def get_zombie_nouns(self):
        words = nltk.word_tokenize(self.sentence)
        tags = nltk.pos_tag(words)
        # zombies are verbs or adjectives that end with following
        zombies = ['ance', 'ment', 'ments', 'tion', 'tions', 'ism', 'ity']
        zombie_nouns = []
        for tag in tags:
            word = tag[0]
            tag = tag[1]
            if tag.startswith('VB') or tag.startswith('JJ'):
                if any(word.endswith(zombie) for zombie in zombies):
                    zombie_nouns.append(word)
        return zombie_nouns


class Paragraph(object):
    """Class that represents a paragraph. It keeps track of compulsive hedgers, intensifiers, abstract nouns,
    zombie nouns, vague words, Flesch reading ease and Dale Chall readability score of a paragraph. It also
    keeps track of total words, sentences, longest sentence and avg words per sentence in a paragraph. """

    def __init__(self, paragraph):
        paragraph = paragraph.replace('—', ' ')
        sentences = nltk.sent_tokenize(paragraph)
        self.sentences = [Sentence(sentence) for sentence in sentences]
        # Flattening list of lists
        self.compulsive_hedgers = list(itertools.chain(*[sentence.compulsive_hedgers for sentence in self.sentences
                                                         if sentence.compulsive_hedgers]))
        self.intensifiers = list(itertools.chain(*[sentence.intensifiers for sentence in self.sentences
                                                   if sentence.intensifiers]))
        self.zombie_nouns = list(itertools.chain(*[sentence.zombie_nouns for sentence in self.sentences
                                                   if sentence.zombie_nouns]))
        self.vague_words = list(itertools.chain(*[sentence.vague_words for sentence in self.sentences
                                                  if sentence.vague_words]))
        self.flesch_reading_score = FleschReading(paragraph).grade()
        self.dale_chall_readability_score = DaleChall(paragraph).grade()
        self.total_words = sum([sentence.total_words for sentence in self.sentences])
        self.total_sentences = len(self.sentences)
        self.total_and_words = sum([sentence.total_and_words for sentence in self.sentences if sentence.total_and_words])
        self.avg_words_per_sentence = round(self.total_words/ self.total_sentences, 2)
        self.longest_sentence = max(sentences)

    def __repr__(self):
        return "sentences= {sentences}, flesch_reading_score={flesch_reading}, dale_chall={dale_chall}".format(
            sentences=self.total_sentences, flesch_reading=self.flesch_reading_score,
            dale_chall=self.dale_chall_readability_score)


class Article(object):
    """
    An article represents a block of tests, i.e. an essay or an article, consisting of paragraphs. For example, it could
    be an essay or a blog post.

    This class keeps track of paragraphs, total sentences, Flesch reading ease, Dale Chall readability score, avg
    sentences per para, avg words per sentence, compulsive hedgers, zombie nouns, abstract nouns, and vague words.
    """
    def __init__(self, name, author, text):
        self.name = name
        self.author = author
        # Replacing em dash and en dash
        text = text.replace('—', ' ')
        self.text = text
        paragraphs = nltk.tokenize.blankline_tokenize(text)
        self.paragraphs = [Paragraph(paragraph) for paragraph in paragraphs]
        self.total_paragrpahs = len(self.paragraphs)
        self.total_words = sum([paragraph.total_words for paragraph in self.paragraphs])
        self.total_sentences = sum([paragraph.total_sentences for paragraph in self.paragraphs])
        self.flesch_reading_score = FleschReading(self.text).grade()
        self.dale_chall_readability_score = DaleChall(self.text).grade()
        self.read_time = self.total_words / 200 # gets us minutes (since we read 200 words per minute so 600 / 200 is 3
        # minutes of reading time)
        self.avg_sentences_per_para = round(self.total_sentences / self.total_paragrpahs, 2)
        self.avg_words_per_sentence = round(self.total_words / self.total_sentences, 2)
        # Flattening list of lists
        self.zombie_nouns = list(itertools.chain(*(paragraph.zombie_nouns for paragraph in self.paragraphs
                                                   if paragraph.zombie_nouns)))
        self.total_zombie_nouns = len(self.zombie_nouns)
        self.compulsive_hedgers = list(itertools.chain(*(paragraph.compulsive_hedgers for paragraph in self.paragraphs
                                                         if paragraph.compulsive_hedgers)))
        self.total_compulsive_hedgers = len(self.compulsive_hedgers)
        self.intensifiers = list(itertools.chain(*(paragraph.intensifiers for paragraph in self.paragraphs
                                                   if paragraph.intensifiers)))
        self.total_intensifiers = len(self.intensifiers)
        self.vague_words = list(itertools.chain(*(paragraph.vague_words for paragraph in self.paragraphs
                                                  if paragraph.vague_words)))
        self.total_vague_words = len(self.vague_words)
        self.and_words = [paragraph.total_and_words for paragraph in self.paragraphs if paragraph.total_and_words]
        self.total_and_words = sum(self.and_words)
        self.and_frequency = str(round(self.total_and_words / self.total_words * 100, 2)) + " %"

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
                    pass # Perhaps this word is not in the cmudict
        return [item[0] for item in list(reversed(sorted(syllable_data.items(), key=operator.itemgetter(1))))[:10]]

    def print_paragraph_stats(self):
        """This method, along with print_article_stats(), can be called to present paragraph stats on a command line.
        Ideally first call print_article_stats() and then this method.
        It shows sentence, avg words per sentence, longest sentence, and readability scores (Flesch reading ease and
        Dale Chall readability scores) of paragraphs.
        """

        sentence_tag = Color('{blue}sentences{/blue}')
        word_tag = Color('{blue}words{/blue}')
        avg_word_tag = Color('{blue}Avg words per sentence{/blue}')
        long_tag = Color('{red}longest{/red}')
        table_data = [
            [Color('{autocyan}Paragraph Stats{/autocyan}')],
            ['Paragraph #', '']
        ]
        for item, para in enumerate(self.paragraphs):
            sentences = Color('{red}%s{/red}' % str(para.total_sentences)) if para.total_sentences > 5 else str(para.total_sentences)
            avg_words_per_sentence = Color(
                '{red}%s{/red}' % str(para.avg_words_per_sentence)) if para.avg_words_per_sentence > 25 else str(
                para.avg_words_per_sentence)
            table_data.append([item + 1,
                               '{sentences} {sent_tag}. {words} {word_tag}. {avg_words} {avg_word_tag}. '
                               '"{longest_sent}..." is the {long_tag} sentence.'.format(
                                   sentences=sentences, sent_tag=sentence_tag, words=para.total_words,
                                   word_tag=word_tag, avg_words=avg_words_per_sentence, avg_word_tag=avg_word_tag,
                                   longest_sent=para.longest_sentence[0:10], long_tag=long_tag
                               )])
            table_data.append(["", "Flesh Reading score={flesch_reading}, Dale Chall Readability= {dale_chall}".format(
                flesch_reading=para.flesch_reading_score, dale_chall=para.dale_chall_readability_score
            )])

        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = True
        table_instance.inner_row_border = True
        table_instance.justify_columns = {0: 'center', 1: 'left'}
        print(table_instance.table)

    def print_article_stats(self):
        """This method is called to present article stats on a command line."""
        banner = """
                 _   _
                | | | | ___  _ __ ___   ___ _ __
                | |_| |/ _ \| '_ ` _ \ / _ \ '__|
                |  _  | (_) | | | | | |  __/ |
                |_| |_|\___/|_| |_| |_|\___|_|

        """
        # print(banner)
        table_data = [
            [Color('{autocyan}Overall Stats{/autocyan}')],
            ['Reading time (in mins)', self.read_time],
            ['Flesch Reading Score', self.flesch_reading_score],
            ['Dale Chall Readability Score', self.dale_chall_readability_score],
            ['Paragraphs', self.total_paragrpahs],
            ['Sentences', self.total_sentences],
            ['Avg sentences per para', self.avg_sentences_per_para],
            ['Avg words per sentence', self.avg_words_per_sentence],
            ['Words', self.total_words],
            ['Zombie nouns', len(self.zombie_nouns)],
            ['"and" frequency"', self.and_frequency],
            ['Compulsive Hedgers', self.total_compulsive_hedgers],
            ['Intensifiers', self.total_intensifiers],
            ['Vague words', self.total_vague_words],

        ]
        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = True
        table_instance.inner_row_border = True
        table_instance.justify_columns = {0: 'left', 1: 'center'}
        print(table_instance.table)
        self.print_detail()

    def print_detail(self):
        if len(self.zombie_nouns) >= 1:
            msg = '{red} **- Zombie nouns: %s {/red}\r\n' % ', '.join(str(zombie) for zombie in self.zombie_nouns)
            print(Color(msg))

        if len(self.compulsive_hedgers) >= 1:
            msg = '{red} **- Compulsive Hedgers: %s {/red}\r\n' % ', '.join(str(compulsive_hedger) for compulsive_hedger in self.compulsive_hedgers)
            print(Color(msg))

        if len(self.intensifiers) >= 1:
            msg = '{red} **- Intensifiers: %s {/red}\r\n' % ', '.join(str(intensifier) for intensifier
                                                                      in self.intensifiers)
            print(Color(msg))

        if len(self.vague_words) >= 1:
            msg = '{red} **- Vague words: %s {/red}\r\n' % ', '.join(str(vague_word) for vague_word in self.vague_words)
            print(Color(msg))

        ten_words_with_most_syllables = self.ten_words_with_most_syllables()
        if len(ten_words_with_most_syllables) >= 1:
            msg = '{red} **- 10 words with most syllables: %s {/red}\r\n' % ', '.join(ten_words_with_most_syllables)
            print(Color(msg))

        msg = "{red} **- Twenty most repeated words (highest to lowest): %s {/red}\r\n" % \
              ', '.join(self.get_n_most_repeated_words(20))
        print(Color(msg))

    def get_n_most_repeated_words(self, n):
        """Gets us n most repeated words in the text. """
        words = nltk.word_tokenize(self.text)
        stopwords = nltk.corpus.stopwords.words('english')
        all_words_except_stop = nltk.FreqDist(w.lower() for w in words if w[0].isalpha() and w not in stopwords)
        return [word for word, freq in all_words_except_stop.most_common(n)]

article = Article('name', 'author', open('/Users/waqas/code/homer/experiment/oped.txt').read())
# article = Article('name', 'author', open('/Users/waqas/PycharmProjects/sense_of_style/experiment/economic_survey_pk_2018_19/overview_of_economy.txt').read())
article.print_article_stats()
# # print(article.words_with_most_syllables())
article.print_paragraph_stats()
