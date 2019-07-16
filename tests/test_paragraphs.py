import unittest
from homer import homer

class TestParagraphs(unittest.TestCase):


    def test_word_count(self):
        sentences = [
            {
                    'para': '''Life is short, as everyone knows. When I was a kid I used to wonder about this. Is life actually short, or are we really complaining about its finiteness? Would we be just as likely to feel life was short if we lived 10 times as long?''',
                    'words': 47,
                    'sentences': 4
            },
            {
                'para': '''Having kids showed me how to convert a continuous quantity, time, into discrete quantities. You only get 52 weekends with your 2 year old. If Christmas-as-magic lasts from say ages 3 to 10, you only get to watch your child experience it 8 times. And while it's impossible to say what is a lot or a little of a continuous quantity like time, 8 is not a lot of something. If you had a handful of 8 peanuts, or a shelf of 8 books to choose from, the quantity would definitely seem limited, no matter what your lifespan was.''',
                'words': 98,
                'sentences': 5
            },
            {
                'para': '''Ok, so life actually is short. Does it make any difference to know that?''',
                'words': 14,
                'sentences': 2
            },
            {
                'para': '''Call me Ishmael. Some years ago—never mind how long precisely— having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off—then, I account it high time to get to sea as soon as I can. This is my substitute for pistol and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship. There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or other, cherish very nearly the same feelings towards the ocean with me.''',
                'words': 201,
                'sentences': 8
            }
        ]

        for data in sentences:
            para = homer.Paragraph(data['para'])
            # for p in para.sentences:
            #     print(p.words)
            self.assertEqual(data['words'], para.total_words)
            self.assertEqual(data['sentences'], para.total_sentences)

if __name__ == "__main__":
    unittest.main()