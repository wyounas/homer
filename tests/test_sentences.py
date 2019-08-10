import unittest
from homer import analyzer


class TestSentences(unittest.TestCase):
    def test_word_count(self):
        sentences = [
            {
                    'line': 'Big or small, Panda is adorable.',
                    'words': 6
            },
            {
                'line': 'I love winter.',
                'words': 3
            },
            {
                'line': 'Do you like great books?',
                'words': 5
            },
            {
                'line': 'He said, "I wish I was there."',
                'words': 7
            },
            {
                'line': 'Thank you!',
                'words': 2
            }
        ]

        for data in sentences:
            sentence_obj = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], len(sentence_obj))

    def test_adjective(self):
        sentences = [
            {
                'line': 'Big or small, Panda is adorable.',
                'words': 0
            },
            {
                'line': 'I love winter and summer.',
                'words': 1
            },
            {
                'line': 'Do you like great and old books? And new ones?',
                'words': 2
            },
            {
                'line': 'He said, "And I wish I was there. And had money"',
                'words': 2
            },
            {
                'line': 'Thank you and I look forward to hearing from you!',
                'words': 1
            }
        ]

        for data in sentences:
            sentence_obj = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], sentence_obj.total_and_words)

    def test_compulsive_hedgers(self):
        sentences = [
            {
                'line': 'Big or small, Panda is apparently adorable.',
                'words': 1
            },
            {
                'line': 'I almost love winter and summer.',
                'words': 1
            },
            {
                'line': 'Partially true, or nearly true; rather I would say almost.',
                'words': 4
            },
            {
                'line': 'He said, "And I wish I was predominantly correct in proposing my theory."',
                'words': 1
            },
            {
                'line': 'Thank you for seemingly great gesture!',
                'words': 1
            }
        ]
        for data in sentences:
            sentence = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], len(list(sentence.get_compulsive_hedgers())), data['line'])

    def test_intensifiers(self):
        sentences = [
            {
                'line': 'Big or small, Panda is extremely adorable.',
                'words': 1
            },
            {
                'line': 'I highly recommend this book.',
                'words': 1
            },
            {
                'line': 'He is very highly recommended',
                'words': 2
            },

        ]
        for data in sentences:
            sentences = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], len(list(sentences.get_intensifiers())), data['line'])

    def test_abstract_nouns(self):
        sentences = [
            {
                'line': 'In this context, I would prefer chocolate.',
                'words': 1
            },
            {
                'line': 'There are many useful frameworks available in Python world.',
                'words': 1
            },
            {
                'line': 'This approach looks good to me.',
                'words': 1
            },
            {
                'line': 'My assumption could be wrong, but this framework and strategy does not solve our problem.',
                'words': 3

            },
            {
                'line': 'Tendency to get fat is dangerous, this condition can lead to a non-desirable condition.',
                'words': 3
            },
            {
                'line': 'What are the variables in this equation?',
                'words': 1
            },
            {
                'line': 'My role is not clear.',
                'words': 1
            }

        ]

        for data in sentences:
            sentences = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], len(list(sentences.get_vague_words())), data['line'])

    def test_ands(self):
        sentences = [
            {
                'line': 'I have eating lot of food and chocolate.',
                'words': 1
            },
            {
                'line': 'I completed reading this book, and that book and that one too.',
                'words': 2
            },
            {
                'line': 'And this is the end.',
                'words': 1
            }

        ]
        for data in sentences:
            sentences = analyzer.Sentence(data['line'])
            self.assertEqual(data['words'], sentences.total_and_words, data['line'])
    #     ands = ['and', 'And']
    #     for _and in ands:
    #         word = homer.Word(_and)
    #         self.assertTrue(word.is_and)

if __name__ == "__main__":
    unittest.main()
