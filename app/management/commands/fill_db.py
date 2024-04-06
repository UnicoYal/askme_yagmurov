from django.core.management import BaseCommand
from app.models import Profile, Question, Answer, Tag, Mark
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
    self.calculate_questions_ratings()
    self.calculate_answers_ratings()
    self.boost_hottest_questions()

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
    users = User.objects.all()
    answers = Answer.objects.all()
    questions = Question.objects.all()
    marks = []
    values = [-1, 1]

    print('Create marks')
    for i in range(count):
      user = random.choice(users)
      value = random.choice(values)
      if random.choice([True, False]):  # рандомно выбираем между вопросами и ответами
          question = random.choice(questions)
          marks.append(Mark(user=user, question=question, value=value))
      else:
          answer = random.choice(answers)
          marks.append(Mark(user=user, answer=answer, value=value))

    Mark.objects.bulk_create(marks[:200000])
    print('200_000')
    Mark.objects.bulk_create(marks[200000:400000])
    print('400_000')
    Mark.objects.bulk_create(marks[400000:600000])
    print('600_000')
    Mark.objects.bulk_create(marks[600000:800000])
    print('800_000')
    Mark.objects.bulk_create(marks[800000:1000000])
    print('1_000_000')
    Mark.objects.bulk_create(marks[1000000:1200000])
    print('1_200_000')
    Mark.objects.bulk_create(marks[1200000:1400000])
    print('1_400_000')
    Mark.objects.bulk_create(marks[1400000:1600000])
    print('1_600_000')
    Mark.objects.bulk_create(marks[1600000:1800000])
    print('1_800_000')
    Mark.objects.bulk_create(marks[1800000:])
    print('2_000_000')

    print('Finish marks')


  def calculate_questions_ratings(self):
    print('Start calculate questions ratings')

    questions_with_sum_marks = Question.objects.annotate(
      total_marks=Coalesce(Sum('mark__value'), 0)
    )

    for question in questions_with_sum_marks:
      if question.total_marks != 0:
        question.rating = question.total_marks
        question.save(update_fields=['rating'])

    print('Finish calculate questions ratings')

  def calculate_answers_ratings(self):
    print('Start calculate answers ratings')

    answers_with_sum_marks = Answer.objects.annotate(
      total_marks=Coalesce(Sum('mark__value'), 0)
    )

    for answer in answers_with_sum_marks:
      if answer.total_marks != 0:
        answer.rating = answer.total_marks
        answer.save(update_fields=['rating'])

    print('Finish calculate answers ratings')

  def boost_hottest_questions(self):
    print('Start boosting questions ratings')

    questions = Question.objects.all()[3000:3030]
    for question in questions:
      question.rating = 3
      question.save(update_fields=['rating'])
      for i in range(3):
        Mark.objects.create(question=question, value=1, user=question.user)

    print('Finish boosting questions ratings')
