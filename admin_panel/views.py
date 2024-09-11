from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ChatConversation, PredefinedMessage, User, ChatbotUser, Administrateur, Message
from .forms import PredefinedMessageForm, CustomUserCreationForm, ChatbotUserForm, AdministrateurForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.paginator import Paginator
import json
from django.shortcuts import render
from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user) 
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'admin_panel/connexion.html')

@login_required
def acceuil(request):
    return render(request, 'admin_panel/acceuil.html')

def deconnexion(request):
    logout(request) 
    return redirect('connexion')

User = get_user_model() 

def is_super_admin(user):
    return user.is_authenticated and user.is_super_admin

User = get_user_model()

@login_required
def dashboard(request):
    # Conversations
    conversations = ChatConversation.objects.all()

    # Utilisateurs (exclure les super admins)
    users = User.objects.filter(is_superuser=False)


    # Administrateurs
    administrateurs = Administrateur.objects.all()

    context = {
        'conversations': conversations,
        'users': users,
        'administrateurs': administrateurs,
    }

    return render(request, 'admin_panel/dashboard.html', context)



def is_super_admin(user):
    return user.is_authenticated and user.is_superuser

def view_conversations(request):
    conversations = ChatConversation.objects.all()
    return render(request, 'admin_panel/conversations.html', {'conversations': conversations})

def suggest_human_agent(request, conversation_id):
    conversation = get_object_or_404(ChatConversation, id=conversation_id)
    # Logic to suggest a human agent (e.g., notify the support team)
    return redirect('dashboard')

def edit_predefined_message(request, message_id):
    message = get_object_or_404(PredefinedMessage, id=message_id)
    if request.method == 'POST':
        form = PredefinedMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PredefinedMessageForm(instance=message)
    return render(request, 'admin_panel/edit_message.html', {'form': form})

@user_passes_test(is_super_admin) 
def manage_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@user_passes_test(is_super_admin)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'admin_panel/add_user.html', {'form': form})

@user_passes_test(is_super_admin) 
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('dashboard')


@user_passes_test(is_super_admin) 
def Administrateurs(request):
    administrateur = Administrateur.objects.all()  # Récupérer tous les administrateurs existants
    paginator = Paginator(administrateur, 10)  # Paginer les résultats si nécessaire
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'administrateur': administrateur,
        'page_obj': page_obj,
       
    }

    return render(request, 'admin_panel/Administrateurs.html', context)


def add_administrateur(request): 
   
    context = {
       
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'admin_panel/add_administrateur.html', context)

    if request.method == 'POST':
        nom = request.POST['nom']

        if not nom:
            messages.error(request, 'Prenom est obligatoire')
            return render(request, 'admin_panel/add_administrateur.html', context )
        
        id = request.POST['id']
        prenom = request.POST['prenom']
        email = request.POST['email']
        mot_de_passe = request.POST['mot_de_passe']

        if not prenom:
            messages.error(request, 'Prenom est obligatoire')
            return render(request, 'admin_panel/add_administrateur.html', context)

        Administrateur.objects.create( id=id, nom=nom,
                               prenom=prenom, email=email, mot_de_passe=mot_de_passe )
        
        return redirect('Administrateurs')

def audit_logs(request): 
   
    context = {
       
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'admin_panel/audit_logs.html', context)

    if request.method == 'POST':
        action = request.POST['action']
        data = request.Post['action']
        timestamp = request.Post['timestamp']
        ip_address = request.Post['ip_address']
        
        AuditLog.objects.create( action=action, data=data,
                               timestamp=timestamp, ip_address=ip_address )
        
        return redirect('audit_logs')

def edit_administrateur(request, id):
    administrateur = Administrateur.objects.get(pk=id)
    context = {
        'administrateur ': administrateur ,
        'values': administrateur ,
        
    }
    if request.method == 'GET':
        return render(request, 'admin_panel/edit_administrateur.html', context)
    if request.method == 'POST':
        id = request.POST['id']

        if not id:
            
            return render(request, 'admin_panel/edit_administrateur.html', context)
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email= request.POST['email']
        mot_de_passe=request.POST['mot_de_passe']

        if not nom:
            
            return render(request, 'admin_panel/edit_administrateur.html', context)

        administrateur.id = id
        administrateur.nom = nom
        administrateur.prenom = prenom
        administrateur.email = email
        administrateur.mot_de_passe = mot_de_passe

        administrateur.save()

        return redirect('Administrateurs')


def delete_admin(request, admin_id):
    if request.method == 'POST':
        admin = Administrateur.objects.get(id=admin_id)
        admin.delete()
        return redirect('Administrateurs')
    


def view_messages(request, conversation_id):
    conversation = get_object_or_404(ChatConversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
    return render(request, 'admin_panel/view_messages.html', {'conversation': conversation, 'messages': messages})

def chat_view(request):
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        new_message_content = request.POST.get('message_content')

        message = Message.objects.filter(conversation_id=conversation_id).latest('timestamp')
        message.content = new_message_content
        message.save()

        return HttpResponse("Message mis à jour avec succès.")
    else:
        return HttpResponse("Requête non valide.")
    
 
@user_passes_test(is_super_admin)
def user_management(request):
    if request.method == 'GET':
        users = User.objects.filter(is_superuser=False)
        return render(request, 'admin_panel/manage_users.html', {'users': users})
    elif request.method == 'POST':
        return add_user(request)
    elif request.method == 'DELETE':
        user_id = request.POST.get('user_id')
        return delete_user(request, user_id)

import requests
from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer


def audit_log_view(request):
    audit_logs = AuditLog.objects.all()
    context = {'audit_logs': audit_logs}
    return render(request, 'admin_panel/Audit.html', context)