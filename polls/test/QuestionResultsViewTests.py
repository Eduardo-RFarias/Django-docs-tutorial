from django.test import TestCase
from django.urls import reverse
from .utils import create_question


class QuestionResultsViewTests(TestCase):
    def test_detail_not_found(self):
        '''
        The results view must return a 404 if the question is not found
        '''
        url = reverse('polls:results', args=(0,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
