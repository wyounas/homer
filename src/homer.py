"""

                 _   _
                | | | | ___  _ __ ___   ___ _ __
                | |_| |/ _ \| '_ ` _ \ / _ \ '__|
                |  _  | (_) | | | | | |  __/ |
                |_| |_|\___/|_| |_| |_|\___|_|


Homer analyzes english text (e.g. a blog post or an essay). It gives reading time, number of total sentences,
readability scores, average sentences per paragraph, average words per sentence, compulsive hedgers, zombie nouns,
and vague words.

Homer can help make your text more clear, simple and useful for the reader.

Author: Waqas Younas
Email: waqas.younas@gmail.com
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
    """
    An abstraction of a 'word'. It determines whether a word is a compulsive hedger, an intensifier, an abstract
    noun or a vague word.

    The idea to look for compulsive hedgers, intensifiers and abstract nouns came from Steven Pinker's book
    `The Sense of Style: The Thinking Person's Guide to Writing in the 21st Century`.

    Whereas the idea to look for vague words came after reading both the above book and the following paper:
    https://litlab.stanford.edu/LiteraryLabPamphlet9.pdf
    """

    def __init__(self, word):
        self.syllables = None
        self.word = word.strip().lower()

    def is_and(self):
        return True if self.word == 'and' else False

    def is_compulsive_hedger(self):
        compulsive_hedgers = ['apparently', 'almost', 'fairly', 'nearly', 'partially', 'predominantly', 'presumably',
                              'rather', 'relative', 'seemingly']
        return True if self.word in compulsive_hedgers else False

    def is_intensifier(self):
        intensifiers = ['very', 'highly', 'extremely']
        return True if self.word in intensifiers else False

    def is_vague_word(self):
        abs_nouns = ["approach", 'assumption', 'concept', 'condition', 'context', 'framework', 'issue', 'model',
                     'process', 'range', 'role', 'strategy', 'tendency', 'variable', 'perspective']
        vague_words = ['accrual', 'derivative', 'fair value', 'portfolio', 'audit', 'poverty', 'evaluation',
                       'management', 'monitoring', 'effectiveness', 'performance', 'competitiveness',
                       'reform', 'assistance', 'growth', 'effort', 'capacity', 'transparency',
                       'effectiveness', 'progress', 'stability', 'protection', 'access',
                       'implementation', 'sustainable'] + abs_nouns
        # vague word is either an abstract noun or it's in the above list
        return True if self.word in vague_words else False

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word



@lru_cache(maxsize=256)
def get_word(word):
    return Word(word)


class Sentence(object):
    """
    An abstraction that represents a sentence. It gives us total words, compulsive hedgers, intensifiers,
    abstract nouns, vague words and zombie nouns in a sentence.
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
    """
    This represents a paragraph. It gives us compulsive hedgers, intensifiers, abstract nouns,
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
                                                         if sentence.get_compsulive_hedgers()]))

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
        # reading time in minutes
        return self.total_words / 200

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


class ArticlePrinter(object):
    """Class which can be used to print Article stats on the command line"""

    def __init__(self, article_obj):
        self.article = article_obj

    def print_article_stats(self):
        """This method is called to present overall article stats on a command line."""
        table_data = [
            [Color('{autocyan}Overall Stats{/autocyan}')],
            ['Reading time (in mins)', self.article.reading_time],
            ['Flesch Reading Score', self.article.get_flesch_reading_score()],
            ['Dale Chall Readability Score', self.article.get_dale_chall_reading_score()],
            ['Paragraphs', self.article.total_paragraphs],
            ['Sentences', self.article.total_sentences],
            ['Avg sentences per para', self.article.avg_sentences_per_para],
            ['Avg words per sentence', self.article.avg_words_per_sentence],
            ['Words', self.article.total_words],
            ['Zombie nouns', len(self.article.get_zombie_nouns())],
            ['"and" frequency"', self.article.get_and_frequency()],
            ['Compulsive Hedgers', len(self.article.get_compulsive_hedgers())],
            ['Intensifiers', len(self.article.get_intensifiers())],
            ['Vague words', len(self.article.get_vague_words())]
        ]
        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = True
        table_instance.inner_row_border = True
        table_instance.justify_columns = {0: 'left', 1: 'center'}
        print(table_instance.table)
        self.print_detail()

    def print_paragraph_stats(self):
        """This method, along with print_article_stats(), can be called to present paragraph stats on a command line.
        Ideally first call print_article_stats() and then this method.
        It shows sentence, average words per sentence, longest sentence, and readability scores (Flesch reading ease and
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
        for item, para in enumerate(self.article.paragraphs):
            sentences = Color('{red}%s{/red}' % str(para.total_sentences)) if para.total_sentences > 5 else str(para.total_sentences)
            avg_words_per_sentence = Color(
                '{red}%s{/red}' % str(para.avg_words_per_sentence)) if para.avg_words_per_sentence > 25 else str(
                para.avg_words_per_sentence)
            table_data.append([item + 1,
                               '{sentences} {sent_tag}. {words} {word_tag}. {avg_words} {avg_word_tag}. '
                               '"{longest_sent}..." is the {long_tag} sentence.'.format(
                                   sentences=sentences, sent_tag=sentence_tag, words=para.total_words,
                                   word_tag=word_tag, avg_words=avg_words_per_sentence, avg_word_tag=avg_word_tag,
                                   longest_sent=str(para.longest_sentence)[0:10], long_tag=long_tag
                               )])
            table_data.append(["", "Flesh Reading score={flesch_reading}, Dale Chall Readability= {dale_chall}".format(
                flesch_reading=para.get_flesch_reading_score(), dale_chall=para.get_dale_chall_reading_score()
            )])

        table_instance = SingleTable(table_data)
        table_instance.inner_heading_row_border = True
        table_instance.inner_row_border = True
        table_instance.justify_columns = {0: 'center', 1: 'left'}
        print(table_instance.table)

    def print_detail(self):
        zombie_nouns = self.article.get_zombie_nouns()
        if len(zombie_nouns) >= 1:
            msg = '{red} **- Zombie nouns: %s {/red}\r\n' % ', '.join(str(zombie) for zombie in zombie_nouns)
            print(Color(msg))

        compulsive_hedgers = self.article.get_compulsive_hedgers()
        if len(compulsive_hedgers) >= 1:
            msg = '{red} **- Compulsive Hedgers: %s {/red}\r\n' % ', '.join(str(compulsive_hedger) for compulsive_hedger in compulsive_hedgers)
            print(Color(msg))

        intensifiers = self.article.get_intensifiers()
        if len(intensifiers) >= 1:
            msg = '{red} **- Intensifiers: %s {/red}\r\n' % ', '.join(str(intensifier) for intensifier
                                                                      in intensifiers)
            print(Color(msg))

        vague_words = self.article.get_vague_words()
        if len(vague_words) >= 1:
            msg = '{red} **- Vague words: %s {/red}\r\n' % ', '.join(str(vague_word) for vague_word in vague_words)
            print(Color(msg))

        ten_words_with_most_syllables = self.article.ten_words_with_most_syllables()
        if len(ten_words_with_most_syllables) >= 1:
            msg = '{red} **- 10 words with most syllables: %s {/red}\r\n' % ', '.join(ten_words_with_most_syllables)
            print(Color(msg))

        msg = "{red} **- Twenty most repeated words (highest to lowest): %s {/red}\r\n" % \
              ', '.join(self.article.get_n_most_repeated_words(20))
        print(Color(msg))


########## Following will be removed from the Final code ##############

editorial_1_july = "/Users/waqas/code/homer/experiment/newspapers/editorial_1_july_19_br.txt"
editorial_2_july = "/Users/waqas/code/homer/experiment/newspapers/editorial_2nd_july_19.txt"
editorial_29_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_29th_july_br.txt"
editorial_25_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_25_br.txt"
editorial_26_june = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_26_br.txt"
editorial_28_jne = "/Users/waqas/code/homer/experiment/newspapers/editorial_june_28_br.txt"


oped_9_feb_hafiz_pasha = "/Users/waqas/code/homer/experiment/newspapers/more_stagflation_9_feb_2019_br_hafiz_pasha"
oped_2_july_hafiz_pasha = "/Users/waqas/code/homer/experiment/newspapers/stab_effort_2_july_19_hafiz_pasha_br.txt"
oped_1_july_anjum = "/Users/waqas/code/homer/experiment/newspapers/tax_man_anjum_ibrahim_1_july_19_br.txt"
oped_1_july_andeel = "/Users/waqas/code/homer/experiment/newspapers/changing_perception_andeel_1_july_19_br.txt"

oped_dawn_5_july_sakib = '/Users/waqas/code/homer/experiment/newspapers/dawn_oped_sakib_sherani_5_july.txt'
oped_dawn_5_july_jihad_azour = '/Users/waqas/code/homer/experiment/newspapers/dawn_oped_jihad_azour_5_july.txt'
shabaz_4_july = '/Users/waqas/code/homer/experiment/newspapers/shabaz_july4_ecc_rejects.txt'

# econ survey
fiscal_dev = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/fiscal_development.txt'
inflation = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/inflation.txt'
manufacturing_and_mining = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/manufacturing_and_mining.txt'
money_and_credit = '/Users/waqas/code/homer/experiment/economic_survey_pk_2018_19/money_and_credit.txt'


# article = Article('Editorial', 'BR', open(shabaz_4_july).read())
article = ArticlePrinter(Article('', '', open(money_and_credit).read()))
# article = Article('name', 'author', open('/Users/waqas/PycharmProjects/sense_of_style/experiment/economic_survey_pk_2018_19/overview_of_economy.txt').read())
article.print_article_stats()
# # print(article.words_with_most_syllables())
article.print_paragraph_stats()
