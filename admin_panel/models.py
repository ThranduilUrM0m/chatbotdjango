from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError

class CustomUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    
class User(AbstractUser):
    is_super_admin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def super_admin_exists(self):
        return self.filter(is_super_admin=True).exists()

    groups = models.ManyToManyField(Group, related_name='admin_panel_user_groups') 
    user_permissions = models.ManyToManyField(
        Permission, related_name='admin_panel_user_permissions' 
    )

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Ensure there is only one super admin
        if self.is_super_admin:
            if self.id is None and User.objects.super_admin_exists():
                raise ValidationError('There can only be one super admin.')
            elif self.id is not None and User.objects.super_admin_exists() and not self.is_super_admin:
                raise ValidationError('There can only be one super admin.')
        super(User, self).save(*args, **kwargs)

class ChatbotUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Make sure to hash passwords

    def __str__(self):
        return self.name

class Administrateur(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=255, default='valeur_par_defaut')
    prenom = models.CharField(max_length=255, default='valeur_par_defaut')
    email = models.CharField(max_length=255, default='valeur_par_defaut')
    mot_de_passe = models.CharField(max_length=255, default='valeur_par_defaut')
  # Make sure to hash passwords

    def __str__(self):
        return self.nom

class AdministrateurPrincipal(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, default='valeur_par_defaut')
    prenom = models.CharField(max_length=255, default='valeur_par_defaut')
    email = models.CharField(max_length=255, default='valeur_par_defaut')
    mot_de_passe = models.CharField(max_length=255, default='valeur_par_defaut')  # Make sure to hash passwords

    def __str__(self):
        return self.nom
class ChatConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation by {self.user.username} at {self.timestamp}"

class Message(models.Model):
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author_chatbot = models.ForeignKey(ChatbotUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure a message has either an author_user or author_chatbot, but not both.
        if not (self.author_user or self.author_chatbot):
            raise ValidationError('A message must have either an author_user or an author_chatbot.')
        if self.author_user and self.author_chatbot:
            raise ValidationError('A message cannot have both an author_user and an author_chatbot.')
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        if self.author_user:
            return f"Message by {self.author_user.username} at {self.timestamp}"
        elif self.author_chatbot:
            return f"Message by {self.author_chatbot.name} at {self.timestamp}"
        return f"Message at {self.timestamp}"

class PredefinedMessage(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
    


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45) 
    action = models.CharField(max_length=100)
    data = models.TextField()


