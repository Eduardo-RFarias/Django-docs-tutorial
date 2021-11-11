import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Choice, Question
from .utils import create_question


class QuestionModelTests(TestCase):
    def test_choices_property(self):
        '''
        Question property choices must return the same as the query Questions.choice_set.all()
        '''
        question = create_question(question_text='test', days=1)
        choice = Choice.objects.create(
            choice_text='test',
            votes=0,
            question=question
        )

        questionChoices = question.choices

        self.assertQuerysetEqual(
            questionChoices,
            question.choice_set.all(),
        )

        self.assertEqual(questionChoices[0], choice)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertTrue(recent_question.was_published_recently())
