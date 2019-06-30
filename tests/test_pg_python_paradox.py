import unittest
from src import homer


class TestPythonParadox(unittest.TestCase):
    analyzed_text = homer.Article("python_paradox", "pg", open('python_paradox.txt').read())

    def test_total_words(self):
        self.assertEqual(182, TestPythonParadox.analyzed_text.total_words)

    def test_total_paragraphs(self):
        self.assertEqual(3, TestPythonParadox.analyzed_text.total_paragrpahs)

    def test_total_sentences(self):
        self.assertEqual(8, TestPythonParadox.analyzed_text.total_sentences)

    def test_average_sentences_in_paragraph(self):
        self.assertEqual(2.67, TestPythonParadox.analyzed_text.avg_sentences_per_para)

    def test_avergae_words_per_sentnece(self):
        self.assertEqual(22.75, TestPythonParadox.analyzed_text.avg_words_per_sentence)

    def test_total_ands(self):
        self.assertEqual(3, TestPythonParadox.analyzed_text.total_and_words)

    def test_zombie_nouns(self):
        self.assertEqual(1, len(TestPythonParadox.analyzed_text.zombie_nouns)) # 'programming'

    def test_intensifiers(self):
        self.assertEqual(0, len(TestPythonParadox.analyzed_text.intensifiers))

    def test_compsulsive_hedgers(self):
        self.assertEqual(0, len(TestPythonParadox.analyzed_text.compulsive_hedgers))

    def test_abstract_nouns(self):
        self.assertEqual(0, len(TestPythonParadox.analyzed_text.abstract_nouns))

if __name__ == "__main__":
    unittest.main()

