from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from django.http import HttpResponse

SIMPLE_QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "tags": ["blabla", "UnicoYal"],
        "text": f"This is question number {i}"
    } for i in range(10)
]

BENDER_QUESTIONS = [
  {
        "id": i,
        "title": f"Question Bender {i}",
        "tags": ["bender"],
        "text": f"This is question number {i}"
    } for i in range(10, 20)
]

QUESTIONS = SIMPLE_QUESTIONS + BENDER_QUESTIONS

ANSWERS = [
    {
        "id": i,
        "text": f"This is answer number {i}"
    } for i in range(20)
]

def paginate(objects, request, per_page=5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        # Если запрашиваемая страница не существует/некорректна, перенаправляем на первую страницу
        page_obj = paginator.page(1)
    return page_obj


def index(request):
  page_obj = paginate(QUESTIONS, request, 3)

  return render(request, "index.html", { "questions": page_obj, "is_auth": 1 })

def hot(request):
  page_obj = paginate(BENDER_QUESTIONS, request, 3)

  return render(request, "hot.html", { "questions": page_obj, "is_auth": 1 })

def question(request, question_id):
  item = QUESTIONS[question_id]
  page_obj = paginate(ANSWERS, request, 3)
  return render(request, "question.html", { "question": item, "answers": page_obj, "is_auth": 1 })

def ask(request):
  return render(request, "ask.html", { "is_auth": 1 })

def signup(request):
  return render(request, "signup.html", { "is_auth": 0 })

def login(request):
  return render(request, "login.html", { "is_auth": 0 })


def settings(request):
  return render(request, "settings.html", { "is_auth": 1 })

def tag(request, tag_name):
  if tag_name == 'bender':
    questions = BENDER_QUESTIONS
  elif tag_name in ["blabla", "UnicoYal"]:
    questions = SIMPLE_QUESTIONS
  else:
    return HttpResponse("No questions with this tag")

  page_obj = paginate(questions, request, 3)
  return render(request, "tag.html", { "questions": page_obj, 'tag_name': tag_name, "is_auth": 1 })

def logout(request):
  # Тут должен будет быть пост запрос и потом редирект в любом случае
  # Пока некая заглушка, чтобы можно было перейти на страницу без использования URL
  return render(request, "login.html", { "is_auth": 0 })

def user(request, user_id):
  return HttpResponse("Просто заглушка")
