from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers
from .views import AuditLogViewSet

router = routers.DefaultRouter()
router.register(r'audit-logs', AuditLogViewSet)

urlpatterns = [
    
    path('', views.connexion, name='connexion'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('conversations/', views.view_conversations, name='conversations'),
    path('conversations/<int:conversation_id>/suggest_human_agent/', views.suggest_human_agent, name='suggest_human_agent'),
    path('messages/<int:conversation_id>/', views.view_messages, name='view_messages'),
    path('messages/chat_view/', views.chat_view, name='chat_view'),
    path('messages/<int:message_id>/edit/', views.edit_predefined_message, name='edit_predefined_message'),
    path('Administrateurs/', views.Administrateurs, name='Administrateurs'),
    path('add_administrateur', views.add_administrateur, name='add_administrateur'),
    path('edit_administrateur/<int:id>', views.edit_administrateur, name='edit_administrateur'),
    path('admin/delete/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('api/', include(router.urls)),
    path('audit_logs/', views.audit_logs, name='audit_logs'),

]
