import unittest
from homer import analyzer


class TestMobyDick(unittest.TestCase):
    analyzed_text = analyzer.Article("moby_dick", "herman_melville", open('moby_dick.txt').read())

    def test_total_words(self):
        self.assertEqual(1647, TestMobyDick.analyzed_text.total_words)

    def test_total_paragraphs(self):
        self.assertEqual(10, TestMobyDick.analyzed_text.total_paragraphs)

    def test_total_sentences(self):
        self.assertEqual(86, TestMobyDick.analyzed_text.total_sentences)

    def test_average_sentences_in_paragraph(self):
        self.assertEqual(8.6, TestMobyDick.analyzed_text.avg_sentences_per_para)

    def test_average_words_per_sentence(self):
        self.assertEqual(19.15, TestMobyDick.analyzed_text.avg_words_per_sentence)

    def test_total_and_words(self):
        print(TestMobyDick.analyzed_text.total_and_words)
        self.assertEqual(55, TestMobyDick.analyzed_text.total_and_words)

    def test_intensifiers(self):
        self.assertEqual(1, len(TestMobyDick.analyzed_text.get_intensifiers()))

    def test_compulsive_hedgers(self):
        self.assertEqual(6, len(TestMobyDick.analyzed_text.get_compulsive_hedgers()))

    def test_longest_sentence(self):
        start = "Whenever I find myself growing grim about the mouth;"
        end = "and methodically knocking people's hats off then, I account it high time to get to sea as soon as I can."
        longest_sentence = str(TestMobyDick.analyzed_text.longest_sentence)
        self.assertTrue(longest_sentence.startswith(start) and longest_sentence.endswith(end))

if __name__ == "__main__":
    unittest.main()

