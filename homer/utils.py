import textstat


class FleschReading(object):
    """
    https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests#Flesch_reading_ease
    """
    def __init__(self, text):
        self.score = textstat.flesch_reading_ease(text)
        self.difficulty_threshold = 60

    def is_difficult(self):
        return True if self.score < self.difficulty_threshold else False

    def grade(self):
        if self.score < 30:
            return 'Very difficult'
        elif 30 <= self.score < 50:
            return 'Difficult'
        elif 50 <= self.score < 60:
            return 'Fairly difficult'
        elif 60 <= self.score < 70:
            return 'Plain English'
        elif 70 <= self.score < 80:
            return 'Fairly easy'
        elif 80 <= self.score < 90:
            return 'Easy'
        elif 90 <= self.score <= 100:
            return 'Very easy'


class DaleChall(object):
    """
    https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula
    """

    def __init__(self, text):
        self.score = round(textstat.dale_chall_readability_score(text), 1)

    def grade(self):
        if self.score <= 4.9:
            return 'Average 4th grade student or lower'
        elif 5.0 <= self.score <= 5.9:
            return 'Average 5th or 6th grade student'
        elif 6.0 <= self.score <= 6.9:
            return 'Average 7th or 8th grade student'
        elif 7.0 <= self.score <= 7.9:
            return 'Average 9th or 10th grade student'
        elif 8.0 <= self.score <= 8.9:
            return 'Average 11th or 12th grade student'
        elif self.score >= 9.0:
            return 'Average 13th or 15th grade student'
