from django.urls import path

from app import views

urlpatterns = [
  path('', views.index, name='index'),
  path('hot/', views.hot, name='hot'),
  path('tag/<str:tag_name>', views.tag, name='tag'),
  path('questions/<int:question_id>', views.question, name='question'),
  path('login/', views.login, name='login'),
  path('signup/', views.signup, name='signup'),
  path('ask/', views.ask, name='ask'),
  path('settings/', views.settings, name='settings'),

  # Просто заглушки
  path('logout/', views.logout, name='logout'),
  path('users/<int:user_id>', views.user, name='user')
]
