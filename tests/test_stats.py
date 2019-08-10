import os
import unittest
from homer import analyzer


class TestTextStats(unittest.TestCase):
    analyzed_text = analyzer.Article("some_text", "economist", open('stats.txt').read())

    def test_total_words(self):
        self.assertEqual(156, TestTextStats.analyzed_text.total_words)

    def test_total_paragraphs(self):
        self.assertEqual(2, TestTextStats.analyzed_text.total_paragraphs)

    def test_total_sentences(self):
        self.assertEqual(18, TestTextStats.analyzed_text.total_sentences)

    def test_average_sentences_in_paragraph(self):
        self.assertEqual(9.0, TestTextStats.analyzed_text.avg_sentences_per_para)

    def test_average_words_per_sentence(self):
        self.assertEqual(8.67, TestTextStats.analyzed_text.avg_words_per_sentence)

    def test_total_and_words(self):
        self.assertEqual(10, TestTextStats.analyzed_text.total_and_words)

    def test_intensifiers(self):
        self.assertEqual(2, len(TestTextStats.analyzed_text.get_intensifiers()))

    def test_compulsive_hedgers(self):
        self.assertEqual(4, len(TestTextStats.analyzed_text.get_compulsive_hedgers()))

if __name__ == "__main__":
    unittest.main()

