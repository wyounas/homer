import unittest
from src.homer import DaleChall

class TestDaleChallReadingScore(unittest.TestCase):

    def test_fourth_grade_or_lower(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 4th grade student or lower'
        dale_chall.score = 4.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 4.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 3.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 2.5
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 1.5
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 0
        self.assertEqual(grade_label, dale_chall.grade())

    def test_fifth_or_sixth_grade(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 5th or 6th grade student'
        dale_chall.score = 5.0
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 5.1
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 5.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 5.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 5.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 6.0
        self.assertNotEqual(grade_label, dale_chall.grade())

    def test_seventh_or_eigth(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 7th or 8th grade student'
        dale_chall.score = 6.0
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 6.1
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 6.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 6.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 6.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 7.0
        self.assertNotEqual(grade_label, dale_chall.grade())

    def test_nine_or_tenth(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 9th or 10th grade student'
        dale_chall.score = 7.0
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 7.1
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 7.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 7.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 7.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 8.0
        self.assertNotEqual(grade_label, dale_chall.grade())

    def test_eleventh_or_twelve(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 11th or 12th grade student'
        dale_chall.score = 8.0
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 8.1
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 8.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 8.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 8.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 9.0
        self.assertNotEqual(grade_label, dale_chall.grade())

    def test_thirteenth_or_fifteen(self):
        dale_chall = DaleChall("Some dummy text")
        grade_label = 'Average 13th or 15th grade student'
        dale_chall.score = 9.0
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 9.1
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 9.4
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 9.8
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 9.9
        self.assertEqual(grade_label, dale_chall.grade())
        dale_chall.score = 10.0
        self.assertNotEqual(grade_label, dale_chall.grade())

if __name__ == "__main__":
    unittest.main()