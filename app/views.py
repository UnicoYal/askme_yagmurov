from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from django.http import HttpResponse
from app.models import Question

def index(request):
  latest_questions = Question.objects.get_latest()
  page_obj = paginate(latest_questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    "is_auth": 1,
    }

  return render(request, "index.html", context)

def hot(request):
  hottest_questions = Question.objects.get_hottest()
  page_obj = paginate(hottest_questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    "is_auth": 1
    }

  return render(request, "hot.html", context)

def question(request, question_id):
  try:
    item = Question.objects.get_by_id(question_id)
  except:
    return render(request, "errors/404.html", status=404)

  page_obj = paginate(item.answers.all(), request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "question": item,
    "answers": page_obj,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    "is_auth": 1
    }

  return render(request, "question.html", context)

def tag(request, tag_name):
  questions = Question.objects.by_tag(tag_name)
  page_obj = paginate(questions, request, 3)
  previous_page_url, next_page_url = generate_page_urls(request, page_obj)

  context = {
    "questions": page_obj,
    "tag_name": tag_name,
    "previous_page_url": previous_page_url,
    "next_page_url": next_page_url,
    "is_auth": 1
    }

  return render(request, "tag.html", context)

def ask(request):
  return render(request, "ask.html", { "is_auth": 1 })

def signup(request):
  return render(request, "signup.html", { "is_auth": 0 })

def login(request):
  return render(request, "login.html", { "is_auth": 0 })

def settings(request):
  return render(request, "settings.html", { "is_auth": 1 })

def logout(request):
  # Тут должен будет быть пост запрос и потом редирект в любом случае
  # Пока некая заглушка, чтобы можно было перейти на страницу без использования URL
  return render(request, "login.html", { "is_auth": 0 })

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
