from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Prefetch
from datetime import date

#!---------------------------TAG-------------------------------------!

class TagManager(models.Manager):
  def get_popular_tags(self, count=10):
    question_scores = QuestionMark.objects.values('question').annotate(score_sum=Sum('value'))
    top_questions = Question.objects.filter(id__in=[q['question'] for q in question_scores]).annotate(score_sum=Sum('questionmark__value')).order_by('-score_sum')[:10]
    top_questions = top_questions.prefetch_related(Prefetch('tags', queryset=Tag.objects.all()))

    tags = []
    for question in top_questions:
        tags.extend(question.tags.all())

    return tags

class Tag(models.Model):
  title = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = TagManager()

  def __str__(self):
    return self.title

#!---------------------------QUESTION-------------------------------------!

class QuestionManager(models.Manager):
  def get_latest(self):
      queryset = self.get_queryset().prefetch_related("tags")
      return queryset.order_by('-created_at')

  def by_tag(self, tag_name):
      queryset = self.get_queryset().prefetch_related("tags")
      return queryset.filter(tags__title__exact=tag_name)

  def get_hottest(self):
      queryset = self.get_queryset().prefetch_related("tags")
      question_scores = QuestionMark.objects.values('question').annotate(score_sum=Sum('value'))
      top_questions = queryset.filter(id__in=[q['question'] for q in question_scores]).annotate(score_sum=Sum('questionmark__value')).order_by('-score_sum')

      return top_questions

  def get_by_id(self, id):
    queryset = self.get_queryset().prefetch_related("tags", "answers")
    return queryset.get(pk=id)

class Question(models.Model):
  title = models.CharField(max_length=255)
  body = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  tags = models.ManyToManyField(Tag)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = QuestionManager()

  def count_answers(self):
    return self.answers.count()

  def calculate_rating(self):
    score_sum = QuestionMark.objects.filter(question_id=self.id).aggregate(Sum('value', default=0))
    return score_sum['value__sum']

  def __str__(self):
    return self.title

#!---------------------------ANSWER-------------------------------------!

class Answer(models.Model):
  body = models.CharField(max_length=255)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
  is_correct = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def calculate_rating(self):
    score_sum = AnswerMark.objects.filter(answer_id=self.id).aggregate(Sum('value', default=0))
    return score_sum['value__sum']

  def __str__(self):
    return self.body

#!---------------------------MARK-------------------------------------!

class BaseMark(models.Model):
  value = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

class QuestionMark(BaseMark):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
    ]

  def __str__(self):
    return str(self.question_id)

class AnswerMark(BaseMark):
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user', 'answer'], name='unique_user_answer')
    ]

  def __str__(self):
    return str(self.answer_id)
#!---------------------------PROFILE-------------------------------------!

class ProfileManager(models.Manager):
  def get_popular_profiles(self, count=5):
    queryset = self.get_queryset()
    return queryset.order_by('-rating')[:count]

# Для дальнейшей быстроты работы было принято решение добавить rating в Profile
# Чтобы каждый раз не выполнять долгий запрос
# Рейтинг пользователя будет складываться из рейтинга его вопросов и ответов
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.PROTECT)
  avatar = models.ImageField(null=True, blank=True)
  rating = models.IntegerField(default=0)
  bio = models.TextField(blank=True)

  objects = ProfileManager()

  def __str__(self):
    return self.user.username
