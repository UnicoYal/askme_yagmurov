from django.db import models
from django.contrib.auth.models import User
from datetime import date

#!---------------------------TAG-------------------------------------!

class TagManager(models.Manager):
   def get_popular_tags(self, count=10):
      return self.annotate(total_rating=models.Sum('question__rating')).order_by('-total_rating')[:count]

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
      return queryset.order_by('-rating')

  def get_by_id(self, id):
    queryset = self.get_queryset().prefetch_related("tags", "answers")
    return queryset.get(pk=id)

# Для дальнейшей быстроты работы было принято решение добавить rating в Question
# Чтобы каждый раз не выполнять долгий запрос
class Question(models.Model):
  title = models.CharField(max_length=255)
  body = models.TextField()
  rating = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  tags = models.ManyToManyField(Tag)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = QuestionManager()

  def count_answers(self):
    return self.answers.count()

  def __str__(self):
    return self.title

#!---------------------------ANSWER-------------------------------------!

# Для дальнейшей быстроты работы было принято решение добавить rating в Answer
# Чтобы каждый раз не выполнять долгий запрос
class Answer(models.Model):
  body = models.CharField(max_length=255)
  rating = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
  is_correct = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.body

#!---------------------------MARK-------------------------------------!

class Mark(models.Model):
  value = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
  answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    if self.question_id is not None:
      return str(self.question_id)
    elif self.answer_id is not None:
      return str(self.answer_id)
    else:
      return "Некорректная оценка"

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
