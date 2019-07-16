import unittest
from homer.homer import FleschReading

class TestFleschReadingReadingScore(unittest.TestCase):

    def test_fifth_grade(self):
        # 90 >= score <= 100
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Very easy'
        flesch_reading.score = 90
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 91
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 94
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 95
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 95
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 100
        self.assertEqual(grade_label, flesch_reading.grade())

    def test_sixth_grade(self):
        # 80 >= score < 90
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Easy'
        flesch_reading.score = 80
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 81
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 84
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 88
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 89
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 90
        self.assertNotEqual(grade_label, flesch_reading.grade())

    def test_seventh_grade(self):
        # 70 >= score < 80
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Fairly easy'
        flesch_reading.score = 70
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 71
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 74
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 78
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 79
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 80
        self.assertNotEqual(grade_label, flesch_reading.grade())

    def test_eigth_and_ninth(self):
        # 60 >= score < 70
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Plain English'
        flesch_reading.score = 60
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 61
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 64
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 68
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 69
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 70
        self.assertNotEqual(grade_label, flesch_reading.grade())

    def test_tenth_to_twelveth(self):
        # 50 >= score < 60
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Fairly difficult'
        flesch_reading.score = 50
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 51
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 54
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 58
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 59
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 60
        self.assertNotEqual(grade_label, flesch_reading.grade())

    def test_college(self):
        # 30 >= score < 50
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Difficult'
        flesch_reading.score = 30
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 31
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 34
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 38
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 39
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 40
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score =42
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 45
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 47
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 49
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 50
        self.assertNotEqual(grade_label, flesch_reading.grade())

    def test_college_graduate(self):
        # 0 >= score < 30
        flesch_reading = FleschReading("Some dummy text")
        grade_label = 'Very difficult'
        flesch_reading.score = 30
        self.assertNotEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 29
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 21
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 15
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 11
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 7
        self.assertEqual(grade_label, flesch_reading.grade())
        flesch_reading.score = 0
        self.assertEqual(grade_label, flesch_reading.grade())

if __name__ == "__main__":
    unittest.main()