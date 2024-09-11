from django.urls import path
from . import views
from django.urls import include, path


urlpatterns = [
path('load_knowledge_base/', views.load_knowledge_base, name='load_knowledge_base'),
path('save_knowledge_base/', views.save_knowledge_base, name='save_knowledge_base'),
path('find_best_match/', views.find_best_match, name='find_best_match'),
path('get_answer_for_question/', views.get_answer_for_question, name='get_answer_for_question'),
path('chatbot_new/', views.chatbot_new, name='chatbot_new')
]