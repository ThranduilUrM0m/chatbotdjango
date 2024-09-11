from django.contrib import admin
from .models import User, ChatConversation, PredefinedMessage, ChatbotUser, Administrateur, AdministrateurPrincipal, Message, AuditLog

# Register your models here.
admin.site.register(User)
admin.site.register(ChatConversation)
admin.site.register(PredefinedMessage)
admin.site.register(ChatbotUser)
admin.site.register(Administrateur)
admin.site.register(AdministrateurPrincipal)
admin.site.register(Message)
admin.site.register(AuditLog)
