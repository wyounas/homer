import unittest
from homer import analyzer


class TestWords(unittest.TestCase):

    def test_and_word(self):
        and_words = ['and', ' and', 'And', 'And ']
        for and_word in and_words:
            word = analyzer.Word(and_word)
            self.assertTrue(word.is_and())

    def test_compulsive_hedgers(self):
        compulsive_hedgers = ['apparently', 'almost', 'fairly', 'nearly', 'partially', 'predominantly', 'presumably',
                              'rather', 'relative', 'seemingly']
        for compulsive_hedger in compulsive_hedgers:
            word = analyzer.Word(compulsive_hedger)
            self.assertTrue(word.is_compulsive_hedger())

    def test_intensifiers(self):
        intensifiers = ['very', 'highly', 'extremely']
        for intensifier in intensifiers:
            word = analyzer.Word(intensifier)
            self.assertTrue(word.is_intensifier())

    def test_vague_words(self):
        vague_words = ["approach", 'assumption', 'concept', 'condition', 'context', 'framework', 'frameworks', 'issue',
                     'process', 'range', 'role', 'strategy', 'tendency', 'variable']
        for vague_word in vague_words:
            word = analyzer.Word(vague_word)
            self.assertTrue(word.is_vague_word())

    def test_repr(self):
        word = analyzer.Word("Amazing")
        word_obj = analyzer.Word(repr(word))
        self.assertTrue(isinstance(word_obj, analyzer.Word))


if __name__ == "__main__":
    unittest.main()
