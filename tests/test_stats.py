import os
import unittest
from homer import homer


class TestTextStats(unittest.TestCase):
    analyzed_text = homer.Article("some_text", "economist", open('stats.txt').read())

    def test_total_words(self):
        self.assertEqual(156, TestTextStats.analyzed_text.total_words)

    def test_total_paragraphs(self):
        self.assertEqual(2, TestTextStats.analyzed_text.total_paragrpahs)

    def test_total_sentences(self):
        self.assertEqual(18, TestTextStats.analyzed_text.total_sentences)

    def test_average_sentences_in_paragraph(self):
        self.assertEqual(9.0, TestTextStats.analyzed_text.avg_sentences_per_para)

    def test_avergae_words_per_sentnece(self):
        self.assertEqual(8.67, TestTextStats.analyzed_text.avg_words_per_sentence)

    def test_total_zombie_nouns(self):
        print(TestTextStats.analyzed_text.zombie_nouns)
        print(5, len(TestTextStats.analyzed_text.zombie_nouns))

    def test_total_and_words(self):
        print(TestTextStats.analyzed_text.and_words)
        self.assertEqual(10, TestTextStats.analyzed_text.total_and_words)

    def test_intensifiers(self):
        print(TestTextStats.analyzed_text.intensifiers)
        self.assertEqual(2, len(TestTextStats.analyzed_text.intensifiers))

    def test_compsulsive_hedgers(self):
        print(TestTextStats.analyzed_text.compulsive_hedgers)
        self.assertEqual(4, len(TestTextStats.analyzed_text.compulsive_hedgers))

    def test_abstract_nouns(self):
        print(TestTextStats.analyzed_text.abstract_nouns)
        self.assertEqual(9, len(TestTextStats.analyzed_text.abstract_nouns))

if __name__ == "__main__":
    unittest.main()

