import unittest
from homer import homer


class TestMobyDick(unittest.TestCase):
    analyzed_text = homer.Article("moby_dick", "herman_melville", open('moby_dick.txt').read())

    def test_total_words(self):
        self.assertEqual(1647, TestMobyDick.analyzed_text.total_words)

    def test_total_paragraphs(self):
        self.assertEqual(10, TestMobyDick.analyzed_text.total_paragrpahs)

    def test_total_sentences(self):
        self.assertEqual(86, TestMobyDick.analyzed_text.total_sentences)

    def test_average_sentences_in_paragraph(self):
        self.assertEqual(8.6, TestMobyDick.analyzed_text.avg_sentences_per_para)

    def test_avergae_words_per_sentnece(self):
        self.assertEqual(19.15, TestMobyDick.analyzed_text.avg_words_per_sentence)

    def test_total_and_words(self):
        print(TestMobyDick.analyzed_text.and_words)
        self.assertEqual(55, TestMobyDick.analyzed_text.total_and_words)

    def test_zombie_nouns(self):
        self.assertEqual(35, len(TestMobyDick.analyzed_text.zombie_nouns))

    def test_intensifiers(self):
        self.assertEqual(1, len(TestMobyDick.analyzed_text.intensifiers))

    def test_compsulsive_hedgers(self):
        self.assertEqual(6, len(TestMobyDick.analyzed_text.compulsive_hedgers))

    def test_abstract_nouns(self):
        self.assertEqual(0, len(TestMobyDick.analyzed_text.abstract_nouns))

if __name__ == "__main__":
    unittest.main()

