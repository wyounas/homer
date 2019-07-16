from colorclass import Color
from terminaltables import SingleTable


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