from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from app.models import Question, Answer, Profile, QuestionMark, AnswerMark
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.forms.forms import NON_FIELD_ERRORS
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

from .forms import UserForm, QuestionForm, AnswerForm

@require_http_methods(['GET'])
def index(request):
  latest_questions = Question.objects.get_latest()
  page_obj = paginate(latest_questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    }

  return render(request, "index.html", context)

@require_http_methods(['GET'])
def hot(request):
  hottest_questions = Question.objects.get_hottest()
  page_obj = paginate(hottest_questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    }

  return render(request, "hot.html", context)

@csrf_protect
@login_required
@require_http_methods(['GET', 'POST'])
def question(request, question_id):
  try:
    item = Question.objects.get_by_id(question_id)
  except:
    raise Http404('Question does not exists')

  page_obj = paginate(item.answers.all().order_by('-created_at'), request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)
  if request.method == "POST":
    if create_answer(request, item):
      return redirect(request.META['HTTP_REFERER'])
  else:
    answer_form = AnswerForm.CreateForm()

  context = {
    "question": item,
    "answers": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    "form": answer_form,
    }

  return render(request, "question.html", context)

@require_http_methods(['GET'])
def tag(request, tag_name):
  questions = Question.objects.by_tag(tag_name)
  page_obj = paginate(questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "tag_name": tag_name,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    }

  return render(request, "tag.html", context)

@login_required
@csrf_protect
@require_http_methods(['GET', 'POST'])
def ask(request):
  if request.method == "POST":
    question_id = create_question(request)
    return redirect(reverse('question', args=[str(question_id)]))
  else:
    ask_form = QuestionForm.AskForm()

  return render(request, "ask.html", context={'form': ask_form})

@csrf_protect
@require_http_methods(['GET', 'POST'])
def signup(request):
  if request.method == "POST":
    register_form = UserForm.RegistrationForm(request.POST, request.FILES)
    if register_form.is_valid():
      user = register_form.save()
      username = user.username
      password = user.password
      auth.authenticate(request, username=username, password=password)
      if user:
        auth.login(request, user)
        return redirect(reverse('index'))
  else:
    register_form = UserForm.RegistrationForm()

  return render(request, "signup.html", context={'form': register_form})

@csrf_protect
@require_http_methods(['GET', 'POST'])
def login(request):
  if request.method == "POST":
    login_form = UserForm.LoginForm(request.POST)
    if login_form.is_valid():
      user = auth.authenticate(request, **login_form.cleaned_data)
      if user:
        auth.login(request, user)
        if request.GET:
          return redirect(reverse(request.GET.get('continue')))
        else:
          return redirect(reverse('index'))
      else:
        login_form.add_error(NON_FIELD_ERRORS, 'Incorrect nickname or password')
  else:
    login_form = UserForm.LoginForm();

  return render(request, "login.html", context={'form': login_form})

@login_required
@csrf_protect
@require_http_methods(['GET', 'POST'])
def settings(request):
  if request.method == "POST":
    settings_form = UserForm.SettingsForm(request.POST, request.FILES, instance=request.user)
    if settings_form.is_valid():
      settings_form.save()
      return redirect(request.META['HTTP_REFERER'])
  else:
    settings_form = settings_initial_value(request.user)

  return render(request, "settings.html", context={'form': settings_form})

@login_required
def logout(request):
  auth.logout(request)
  return redirect(request.META['HTTP_REFERER'])

@csrf_protect
@login_required
@require_http_methods(['POST'])
def set_mark(request):
  body = json.loads(request.body)
  if body['operation_type'] == 'like':
    mark_value = 1
  else:
    mark_value = -1;

  if body['item_type'] == 'question':
    item = get_object_or_404(Question, pk=body['item_id'])
    if item.has_mark_by_user(request.user):
      return JsonResponse({"error": "Record not unique"})

    QuestionMark.objects.create(question=item, value=mark_value, user=request.user)
  else:
    item = get_object_or_404(Answer, pk=body['item_id'])
    if item.has_mark_by_user(request.user):
      return JsonResponse({"error": "Record not unique"})

    AnswerMark.objects.create(answer=item, value=mark_value, user=request.user)

  body['likes_count'] = item.calculate_rating()

  return JsonResponse(body)

@csrf_protect
@require_http_methods(['POST'])
def check_mark(request):
  body = json.loads(request.body)
  if body['item_type'] == 'question':
    item = get_object_or_404(Question, pk=body['item_id'])
  else:
    item = get_object_or_404(Answer, pk=body['item_id'])

  user = get_object_or_404(User, pk=body['user_id'])
  is_marked = item.has_mark_by_user(user)

  return JsonResponse({"is_marked": is_marked})

@csrf_protect
@login_required
@require_http_methods(['POST'])
def correct_answer(request):
  body = json.loads(request.body)
  answer = get_object_or_404(Answer, pk=body['answer_id'])
  if answer.question.user.id != request.user.id:
    return JsonResponse({"error": 'You dont have access to this function'})

  answer.is_correct = not answer.is_correct
  answer.save()

  return JsonResponse({"correct": answer.is_correct})


@csrf_protect
@require_http_methods(['POST'])
def check_answer(request):
  body = json.loads(request.body)
  answer = get_object_or_404(Answer, pk=body['answer_id'])
  response = {
    "is_correct": answer.is_correct,
    "is_question_author": answer.question.user.id == request.user.id
  }

  return JsonResponse(response)

def user(request, user_id):
  return HttpResponse("Просто заглушка")

def custom_404(request, exception):
  return render(request, "errors/404.html", status=404)

def generate_page_urls(request, page_obj):
    path = request.path
    previous_page_url = ''
    next_page_url = ''

    query_params = request.GET.copy()
    query_params.pop('page', None)

    if page_obj.has_previous():
      query_params['page'] = page_obj.previous_page_number()
      previous_page_url = f"{path}?{query_params.urlencode()}"

    if page_obj.has_next():
      query_params.pop('page', None)
      query_params['page'] = page_obj.next_page_number()
      next_page_url = f"{path}?{query_params.urlencode()}"

    return previous_page_url, next_page_url

def paginate(objects, request, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        # Если запрашиваемая страница не существует/некорректна, перенаправляем на первую страницу
        page_obj = paginator.page(1)
    return page_obj

def create_question(request):
  form = QuestionForm.AskForm(request.POST)
  if form.is_valid():
    title = form.cleaned_data['title']
    body = form.cleaned_data['body']
    tags = form.cleaned_data['tags']
    question = Question.objects.create(user=request.user, title=title, body=body)
    question.save()
    question.tags.add(*tags)
    return question.id

  raise ValidationError('Cannot create question')

def create_answer(request, question):
  form = AnswerForm.CreateForm(request.POST)
  if form.is_valid():
    body = form.cleaned_data['body']
    answer = Answer.objects.create(user=request.user, body=body, question=question)
    return True

  return False

def settings_initial_value(user):
  initial = model_to_dict(user)
  init = model_to_dict(Profile.objects.get(user=user))
  initial.update(init)

  return UserForm.SettingsForm(initial=initial)
