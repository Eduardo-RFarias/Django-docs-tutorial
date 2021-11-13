from django.contrib.auth.models import User
from polls.models import Question, Choice
from django.utils import timezone

User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')

question = Question.objects.create(
    question_text='Teste', pub_date=timezone.now())

for num in range(1, 3):
    Choice.objects.create(
        question=question,
        choice_text=f'Choice {num}',
        votes=0
    )
