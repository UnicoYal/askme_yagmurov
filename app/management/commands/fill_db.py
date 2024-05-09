from django.core.management import BaseCommand
from app.models import Profile, Question, Answer, Tag, QuestionMark, AnswerMark
from django.contrib.auth.models import User
from faker import Faker
import random
from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce


class Command(BaseCommand):
  fake = Faker()

  def add_arguments(self, parser):
    parser.add_argument('ratio', type=int)

  # handle argument from command prompt
  def handle(self, *args, **options):
    ratio = options['ratio']

    self.create_users(ratio)
    self.create_profiles(ratio)
    self.create_tags(ratio)
    self.create_questions(ratio * 10)
    self.create_answers(ratio * 100)
    self.create_marks(ratio * 200)

  def create_users(self, count):
    print('Create users')
    usernames = set()
    for _ in range(count):
        while True:
            username = self.fake.user_name()
            # Для поддержания уникальности username
            if username not in usernames:
                break
        usernames.add(username)

    users = [
        User(username=username, email=self.fake.email(), password=self.fake.password())
        for username in usernames
    ]

    User.objects.bulk_create(users)
    print('Finish users')

  def create_profiles(self, count):
    print('Create profiles')
    users = User.objects.all()
    profiles = []

    for user in users:
      profile = Profile(user=user)
      profiles.append(profile)

    Profile.objects.bulk_create(profiles)
    print('Finish profiles')

  def create_tags(self, count):
    print('Create tags')

    tag_names = set()
    for _ in range(count):
        while True:
            name = self.fake.word() + self.fake.word()
            if name not in tag_names:
                break

        tag_names.add(name)

    tags = [Tag(title=tag_name) for tag_name in tag_names]
    Tag.objects.bulk_create(tags)

    print('Finish tags')

  def create_questions(self, count):
    users = User.objects.all()
    tags = Tag.objects.all()

    print('Create questions')
    questions = []

    for _ in range(count):
        title = self.fake.sentence()
        body = self.fake.text()
        user = random.choice(users)
        questions.append(Question(title=title, body=body, user=user))

    Question.objects.bulk_create(questions)
    print('Finish creating questions')

    print('Update question tags')

    for question in questions:
      question.tags.set([random.choice(tags) for _ in range(random.randint(1, 3))])

    print('Finish updating tags')

  def create_answers(self, count):
    users = User.objects.all()
    questions = Question.objects.all()
    print('Start answers')

    answers = [Answer(question=random.choice(questions),
                      body=self.fake.text(),
                      user=random.choice(users))
                for _ in range(count)]

    Answer.objects.bulk_create(answers[:100000])
    print('100_000')
    Answer.objects.bulk_create(answers[100000:200000])
    print('200_000')
    Answer.objects.bulk_create(answers[200000:300000])
    print('300_000')
    Answer.objects.bulk_create(answers[300000:400000])
    print('400_000')
    Answer.objects.bulk_create(answers[400000:500000])
    print('500_000')
    Answer.objects.bulk_create(answers[500000:600000])
    print('600_000')
    Answer.objects.bulk_create(answers[600000:700000])
    print('700_000')
    Answer.objects.bulk_create(answers[700000:800000])
    print('800_000')
    Answer.objects.bulk_create(answers[800000:900000])
    print('900_000')
    Answer.objects.bulk_create(answers[900000:])
    print('1_000_000')
    print('Finish answers')

  def create_marks(self, count):
    answers = Answer.objects.all()
    users = User.objects.all()
    questions = Question.objects.all()
    question_marks = []
    answer_marks = []
    qm = 0
    am = 0
    values = [-1, 1]

    print('Create marks')
    for i in range(count):
      print(i)
      value = random.choice(values)
      if random.choice([True, False]):  # рандомно выбираем между вопросами и ответами
          question = questions[i % (len(questions)-1)]
          user = (i % (len(users) - 1))+1
          question_marks.append(QuestionMark(question=question, value=value, user_id=user))
      else:
          answer = answers[i % (len(answers)-1)]
          user = (i % (len(users) - 1))+1
          answer_marks.append(AnswerMark(answer=answer, value=value, user_id=user))

    QuestionMark.objects.bulk_create(question_marks)
    AnswerMark.objects.bulk_create(answer_marks)

    print('Finish marks')
